from typing import Optional, Union
import torch
from transformers.generation.utils import GenerateDecoderOnlyOutput
from transformers.modeling_outputs import CausalLMOutputWithPast

from natllm.validation import RegexValidator


class Generator:
    def __init__(self, model, tokenizer) -> None:
        self.model = model
        self.tokenizer = tokenizer
    
    def generate(
        self,
        inputs: Optional[torch.Tensor] = None,
        max_new_tokens=None,
        do_sample=True,
        top_k=None,
        top_p=None,
        temperature=None,
    ) -> Union[GenerateDecoderOnlyOutput, torch.LongTensor]:
        raise NotImplementedError


class RegexGenerator(Generator):
    def __init__(self, model, tokenizer, regex: str = None) -> None:
        """
        if regex is None, then no validation will be performed
        """
        self.validator = None
        super().__init__(model, tokenizer)
        if regex is not None:
            self.validator = RegexValidator(regex)

    def generate(
        self,
        inputs: Optional[torch.Tensor] = None,
        max_new_tokens=None,
        do_sample=True,
        top_k=None,
        top_p=None,
        temperature: float = 1,
    ) -> Union[GenerateDecoderOnlyOutput, torch.LongTensor]:

        assert inputs is not None and inputs.size(0) == 1, "Batch size must be 1"

        # 由于validation需要输入字符串，因此需要tokenizer
        if self.validator is not None:
            self.validator.init_state()
        past_key_values = None

        # do generation
        for step in range(max_new_tokens):
            if past_key_values is not None:
                pruned_input_ids = inputs[:, past_key_values[0][0].size(2) :]
            else:
                pruned_input_ids = inputs

            output: CausalLMOutputWithPast = self.model(
                input_ids=pruned_input_ids,
                use_cache=True,
                past_key_values=past_key_values,
                return_dict=True,
                output_attentions=False,
                output_hidden_states=False,
            )
            logits = output.logits
            past_key_values = output.past_key_values
            if temperature != 0:
                logits = logits/temperature

            step_logits: torch.Tensor =torch.softmax(logits[0,-1], dim=0)

            while True:
                if top_k is not None and do_sample:
                    cand_probs, cand_index = step_logits.topk(dim=0, k=top_k)
                    cand_probs /= cand_probs.sum()

                    selected_index = torch.multinomial(cand_probs, 1).item()
                    selected_index = cand_index[selected_index]

                elif top_p is not None and do_sample:
                    sorted_probs, sorted_indices = torch.sort(step_logits, descending=True)
                    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
                    sorted_to_remove = cumulative_probs > top_p
                    sorted_to_remove[..., 1:] = sorted_to_remove[..., :-1].clone()
                    sorted_to_remove[..., 0] = 0

                    # 过滤掉超过 top_p 的概率
                    indices_to_remove = sorted_indices[sorted_to_remove]
                    step_logits[indices_to_remove] = 0
                    step_logits = step_logits / step_logits.sum()
                    # 根据新的概率分布进行采样
                    selected_index = torch.multinomial(step_logits, 1).squeeze()

                elif not do_sample or temperature == 0:
                    cand_probs, cand_index = step_logits.topk(dim=0, k=1)
                    selected_index = cand_index.squeeze()

                else:
                    selected_index = torch.multinomial(step_logits, 1).squeeze()

                step_output: int = selected_index  # 根据不同sampling方法得到

                if step_output == self.tokenizer.eos_token_id:
                    if self.validator.finish():
                        break
                elif self.validator.validate(self.tokenizer.decode(step_output)):
                    break
                step_logits[step_output] = 0

            inputs = torch.cat([inputs, step_output[None,None]], dim=1)

            if step_output == self.tokenizer.eos_token_id:
                return GenerateDecoderOnlyOutput(
                    sequences=inputs,
                    past_key_values=past_key_values,
                    attentions=None,
                    hidden_states=None,
                    scores=None
                )
        return GenerateDecoderOnlyOutput(
                    sequences=inputs,
                    past_key_values=past_key_values,
                    attentions=None,
                    hidden_states=None,
                    scores=None
                )
