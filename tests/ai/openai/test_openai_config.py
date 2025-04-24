
from ai.openai.openai_config import OpenAIConfig


def test_openai_config_custom_values():
    config = OpenAIConfig(model="gpt-3.5", temperature=0.5, max_tokens=2048, top_p=0.9)
    assert config.model == "gpt-3.5"
    assert config.temperature == 0.5
    assert config.max_tokens == 2048
    assert config.top_p == 0.9
