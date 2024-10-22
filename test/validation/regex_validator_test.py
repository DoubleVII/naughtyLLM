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


def test_regexValidator_basic2():
    regex = "genshin impact"

    test_tokens = ["gen", "shin ", "impact"]
    validator = RegexValidator(regex)

    validator.init_state()

    for test_token in test_tokens:
        assert validator.validate(test_token)

    assert validator.finish()


def test_regexValidator_basic3():
    regex = r"\d+\*\d+=\d+"

    test_tokens = ["5", "*", "6", "=", "30"]
    validator = RegexValidator(regex)

    validator.init_state()

    for test_token in test_tokens:
        assert validator.validate(test_token)

    assert validator.finish()

def test_regexValidator_basic4():
    regex = r"genshin impact"
    test_tokens = ["genshin", " imp"]
    validator = RegexValidator(regex)

    validator.init_state()

    for test_token in test_tokens:
        assert validator.validate(test_token)

    assert not validator.finish()

def test_regexValidator_basic5():
    regex = r"genshin"
    test_tokens = ["gen","shin"," impact"]
    validator = RegexValidator(regex)

    validator.init_state()

    assert validator.validate(test_tokens[0])
    assert validator.validate(test_tokens[1])
    assert not validator.validate(test_tokens[2])

    assert validator.finish()

def test_regexValidator_recover():
    regex = "123456789"

    test_tokens = ["123", "456", "780", "789"]
    validator = RegexValidator(regex)

    validator.init_state()


    assert validator.validate(test_tokens[0])
    assert validator.validate(test_tokens[1])
    assert not validator.validate(test_tokens[2])
    assert validator.validate(test_tokens[3])

    assert validator.finish()

def test_regexValidator_recover2():
    regex = r"\d+\+\d+=\d+"

    test_tokens = ["32", "+", "7", "-","=","42"]
    validator = RegexValidator(regex)

    validator.init_state()

    assert validator.validate(test_tokens[0])
    assert validator.validate(test_tokens[1])
    assert validator.validate(test_tokens[2])
    assert not validator.validate(test_tokens[3])
    assert validator.validate(test_tokens[4])
    assert validator.validate(test_tokens[5])

    assert validator.finish()

def test_regexValidator_recover3():
    regex = r"start.*end"
    test_tokens = ["sta","3","rt" " middle","","@!#","en","d"]
    validator = RegexValidator(regex)

    validator.init_state()

    assert validator.validate(test_tokens[0])
    assert not validator.validate(test_tokens[1])
    assert validator.validate(test_tokens[2])
    assert validator.validate(test_tokens[3])
    assert validator.validate(test_tokens[4])
    assert validator.validate(test_tokens[5])
    assert validator.validate(test_tokens[6])

    assert validator.finish()

