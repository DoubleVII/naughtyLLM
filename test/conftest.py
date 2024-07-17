import pytest

@pytest.fixture(scope="session")
def test_model_path() -> str:
    return "Felladrin/Llama-68M-Chat-v1"