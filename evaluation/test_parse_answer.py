import pytest
from run_gsm8k_eval import parse_answer  # 根据实际模块路径导入 parse_answer

#   目的: 测试 parse_answer 是否能正确从有效的 JSON 字符串中提取答案。
#   断言: 确保 parse_answer 返回值为 6
def test_parse_answer_valid_json():
    output = '''
    {
        "question": "There are 15 trees in the grove.Grove workers will plant trees in the grove today.After they are done, there will be 21 trees.How many trees did the grove workers plant today?",
        "response": {
            "reasoning": "There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6.",
            "answer": 6
        }
    }
    '''
    assert parse_answer(output) == 6


# 目的: 测试 parse_answer 处理 JSON 中缺少 answer 字段的情况。
# 断言: 确保 parse_answer 返回 None。
def test_parse_answer_missing_answer():
    output = '''
    {
        "question": "There are 15 trees in the grove.Grove workers will plant trees in the grove today.After they are done, there will be 21 trees.How many trees did the grove workers plant today?",
        "response": {
            "reasoning": "There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6."
        }
    }
    '''
    assert parse_answer(output) is None

# 目的: 测试 parse_answer 处理无效 JSON 的情况（例如，JSON 格式不完整）。
# 断言: 确保 parse_answer 返回 None。
def test_parse_answer_invalid_json():
    output = '''
    {
        "question": "There are 15 trees in the grove.Grove workers will plant trees in the grove today.After they are done, there will be 21 trees.How many trees did the grove workers plant today?",
        "response": {
            "reasoning": "There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6.",
            "answer": 6
        }
    '''
    assert parse_answer(output) is None

# 目的: 测试 parse_answer 处理空字符串的情况。
# 断言: 确保 parse_answer 返回 None。
def test_parse_answer_empty_string():
    output = ""
    assert parse_answer(output) is None
