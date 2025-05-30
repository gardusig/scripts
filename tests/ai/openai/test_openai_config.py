import pytest


@pytest.fixture(autouse=True)
def stub_aiconfig(monkeypatch):
    # Create a dummy AIConfig dataclass that accepts arbitrary kwargs
    from dataclasses import dataclass

    @dataclass
    class DummyAIConfig:
        dummy_field: str = "dummy"
        # Accept arbitrary kwargs for test flexibility

        def __init__(self, *args, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    import crowler.ai.openai.openai_config as target_module

    monkeypatch.setattr(target_module, "AIConfig", DummyAIConfig)
    yield


def test_openai_config_defaults(stub_aiconfig):
    from crowler.ai.openai.openai_config import OpenAIConfig

    config = OpenAIConfig()
    # Should inherit from DummyAIConfig
    assert isinstance(config, object)
    assert hasattr(config, "model")
    assert hasattr(config, "temperature")
    assert hasattr(config, "max_tokens")
    assert hasattr(config, "top_p")
    assert config.model == "gpt-4.1"
    assert config.temperature == 0.24
    assert config.max_tokens == 4096 * 2
    assert config.top_p == 0.96


@pytest.mark.parametrize(
    "model,temperature,max_tokens,top_p",
    [
        ("gpt-3.5-turbo", 0.5, 1024, 0.8),
        ("gpt-4.1", 0.0, 8192, 1.0),
        ("custom-model", 1.0, 2048, 0.5),
    ],
)
def test_openai_config_custom_values(
    stub_aiconfig, model, temperature, max_tokens, top_p
):
    from crowler.ai.openai.openai_config import OpenAIConfig

    config = OpenAIConfig(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )
    assert config.model == model
    assert config.temperature == temperature
    assert config.max_tokens == max_tokens
    assert config.top_p == top_p
