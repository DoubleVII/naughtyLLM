import pytest

@pytest.fixture(scope="session")
def test_model_path() -> str:
    return "JackFram/llama-68m"