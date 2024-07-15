
from typing import Optional, Union
import torch
from transformers.generation.utils import GenerateDecoderOnlyOutput

def generate(
        model,
        inputs: Optional[torch.Tensor] = None,
        max_new_tokens=None,
        do_sample=True,
        top_k=None,
        top_p=None,
        temperature=None,
    ) -> Union[GenerateDecoderOnlyOutput, torch.LongTensor]:
    raise NotImplementedError

