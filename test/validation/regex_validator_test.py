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
