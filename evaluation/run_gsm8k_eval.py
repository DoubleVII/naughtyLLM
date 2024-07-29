from typing import Any, Union, Optional, List, Tuple, Dict
import pandas as pd
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import torch
from natllm.generation.utils import RegexGenerator
from tqdm import tqdm

def CLI(*args: Any, **kwargs: Any) -> Any:
    from jsonargparse import CLI

    kwargs.setdefault("as_positional", False)

    return CLI(*args, **kwargs)

prompt = """Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\nA: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6.\n\n
Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\nA: There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is 5.\n\n
Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\nA: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39.\n\n
Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\nA: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is 8.\n\n
Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?\nA: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is 9.\n\n
Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?\nA: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. The answer is 29.\n\n
Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?\nA: Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. The answer is 33.\n\n
Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\nA: Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. The answer is 8.\n\n
Q: {}\nA:"""


guidance_regex = r"[\w\d\.\*\-=\+,\?/ ]{50,700}\. The answer is (\-?[0-9,]+)\."



def parse_answer(output:str) -> Optional[int]:
    output = output.split("\n")[0] # remove extra lines
    answer_regex = r"The answer is (\-?[0-9,]+)\."
    match = re.search(answer_regex, output)
    if match is not None:
        # Extract the first group, remove commas and convert to int
        number_str = match.group(1).replace(',', '')
        return int(number_str)
    else:
        return None

def load_data(data_path: str) -> List[Dict]:
    assert data_path.endswith(".parquet"), "data_path must be a parquet file"
    df = pd.read_parquet(data_path)

    test_data = []

    for i, row in df.iterrows():
        answer_num = row["answer"].split("####")[-1].replace(",", "")
        answer_num = int(answer_num)
        test_data.append({"question": row["question"], "answer": answer_num})
    
    return test_data


def load_model_and_tokenizer(model_path: str) -> Tuple[Any, Any]:
    config = AutoConfig.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype=(
            torch.bfloat16 if config.torch_dtype == torch.bfloat16 else torch.float16
        ),
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer

def run(model: str, data_path: str, max_new_tokens:int = 200, use_regex:bool = True):

    test_data = load_data(data_path)
    model, tokenizer = load_model_and_tokenizer(model)
    regex_generator = RegexGenerator(model, tokenizer, regex=guidance_regex if use_regex else None)

    pass_parsing = 0
    pass_answer = 0

    for test_sample in tqdm(test_data):
        question_text = test_sample["question"]
        answer = test_sample["answer"]

        input_text = prompt.format(question_text)
        model_inputs = tokenizer([input_text], return_tensors="pt").to("cuda")
        generated_ids = regex_generator.generate(model_inputs.input_ids, max_new_tokens=max_new_tokens, do_sample=False)

        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        generated_answer = parse_answer(generated_text)
        if generated_answer is not None:
            pass_parsing += 1
            if generated_answer == answer:
                pass_answer += 1

    print(f"Pass parsing: {pass_parsing}/{len(test_data)} = {pass_parsing/len(test_data)}")
    print(f"Accuracy: {pass_answer}/{len(test_data)} = {pass_answer/len(test_data)}")


if __name__ == "__main__":
    CLI(run)