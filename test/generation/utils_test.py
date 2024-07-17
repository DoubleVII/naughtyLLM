import pytest
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import torch
from natllm.generation.utils import RegexGenerator


@pytest.fixture(scope="module")
def model(test_model_path):
    config = AutoConfig.from_pretrained(test_model_path)
    model = AutoModelForCausalLM.from_pretrained(
        test_model_path,
        device_map="cpu",
        torch_dtype=(
            torch.bfloat16 if config.torch_dtype == torch.bfloat16 else torch.float16
        ),
    )
    return model


@pytest.fixture(scope="module")
def tokenizer(test_model_path):
    tokenizer = AutoTokenizer.from_pretrained(test_model_path)
    return tokenizer


def test_basic_generation(tokenizer, model):

    basic_generator = RegexGenerator(model, tokenizer)

    text = "compute the following math problem: 23+4="
    model_inputs = tokenizer([text], return_tensors="pt").to("cpu")

    ref_generated_ids = model.generate(
        model_inputs.input_ids, max_new_tokens=20, do_sample=False
    )
    ref_generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, ref_generated_ids)
    ]

    generated_ids = basic_generator.generate(model_inputs.input_ids, max_new_tokens=20, do_sample=False)

    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    assert ref_generated_ids == generated_ids
