import interegular.patterns
from natllm.validation import RegexValidator
import pytest

def test_regexValidator_basic():
    regex = ".*"

    test_tokens = ["11", "22", "33", "asd"]
    validator = RegexValidator(regex)

    validator.init_state()

    for test_token in test_tokens:
        assert validator.validate(test_token)

    assert validator.finish()


def test_regexValidator_invalid_regex():
    regex = "*"
    import interegular
    with pytest.raises(interegular.InvalidSyntax):
        validator = RegexValidator(regex)


# 测试匹配运算表达式
def test_regexValidator_expression():
    regex = r"[-+]?(\d+(\.\d+)?)([-+*/][-+]?(\d+(\.\d+)?))*=[-+]?(\d+(\.\d+)?)"
    validator = RegexValidator(regex)
    validator.init_state()

    valid_expressions = [
        "3-4=-1",
        "5*6=30",
        "7/8=0.875",
        "-1+2.5=1.5",
        "3.14*2=6.28",
        "4*5/2=10",
        "-1+2.5-0.5=1",
    ]

    invalid_expressions = [
        "1+2=",      # 没有结果
        "5 *6=30",   # 包含空格
        "3.14.15+2=5.14", # 错误的小数格式
        "abc+1=1",   # 非数字字符
        "1..2=3.2",  # 双小数点
        "1**2=1",    # 连续运算符
        "*2+3=5",    # 开头运算符
    ]

    for expr in valid_expressions:
        assert validator.validate(expr), f"Valid expression failed: {expr}"
        assert validator.finish(), f"Valid expression did not finish correctly: {expr}"

    for expr in invalid_expressions:
        assert not validator.validate(expr), f"Invalid expression passed: {expr}"
        assert not validator.finish(), f"Invalid expression finished correctly: {expr}"
