from typing import Optional, Union
import torch
from transformers.generation.utils import GenerateDecoderOnlyOutput

from validation import RegexValidator


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
    def __init__(self, model, tokenizer, regex: str) -> None:
        self.validator = RegexValidator(regex)

    def generate(
        self,
        inputs: Optional[torch.Tensor] = None,
        max_new_tokens=None,
        do_sample=True,
        top_k=None,
        top_p=None,
        temperature=None,
    ) -> Union[GenerateDecoderOnlyOutput, torch.LongTensor]:
        # 由于validation需要输入字符串，因此需要tokenizer
        
        self.validator.init_state()

        # do generation
        for step in range(max_new_tokens):
            ...

            step_logits: torch.Tensor = ...
            while True:
                step_output: int = ...  # 根据不同sampling方法得到

                if step_output == eos_id:
                    if self.validator.finish():
                        break
                elif self.validator.validate(tokenizer.decode(step_output)):
                    break

                step_logits[step_output] = 0
