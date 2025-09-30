import os.path
from pathlib import Path
from typing import Literal, Dict, Any

import yaml
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek

# Define available LLM types
LLMType = Literal["basic", "reasoning", "websearch"]
# Cache for LLM instances
_llm_cache: dict[LLMType, BaseChatModel] = {}
# cinfig cache
_config_cache: Dict[str, Dict[str, Any]] = {}


def replace_env_vars(value: str) -> str:
    """Replace environment variables in string values."""
    if not isinstance(value, str):
        return value
    if value.startswith("$"):
        env_var = value[1:]
        return os.getenv(env_var, env_var)
    return value

def process_dict(config: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively process dictionary to replace environment variables."""
    if not config:
        return {}
    result = {}
    for key, value in config.items():
        if isinstance(value, dict):
            result[key] = process_dict(value)
        elif isinstance(value, str):
            result[key] = replace_env_vars(value)
        else:
            result[key] = value
    return result

# Load YAML configuration
def load_yaml_config(file_path:str)->Dict[str, Any]:
    """Load YAML configuration from a file."""
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"File {file_path} does not exist.")

    # check if the file exist in cache
    if file_path in _config_cache:
        return _config_cache[file_path]

    # load the file if not in cache
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)

    processed_config = process_dict(config)

    # cache the config
    _config_cache[file_path] = processed_config

    return processed_config


def get_llm_by_type(llm_type: LLMType) -> BaseChatModel:
    """
    Get LLM instance by type. Returns cached instance if available.
    """

    if llm_type in _llm_cache:
        return _llm_cache[llm_type]

    # 使用正确的路径查找 conf.yaml
    config_path = Path(__file__).parent.parent / "conf.yaml"
    config = load_yaml_config(str(config_path))
    llm = _create_llm_use_conf(llm_type, config)
    _llm_cache[llm_type] = llm
    return  llm


def _create_llm_use_conf(llm_type: LLMType, conf: Dict[str, Any]) -> BaseChatModel:
    """
    Create LLM instance based on configuration.
    """

    llm_conf = conf.get(llm_type, {})
    if not llm_conf:
        raise ValueError(f"Invalid LLM type: {llm_type}")


    if llm_type== "basic" or llm_type== "websearch":
        return ChatOpenAI(**llm_conf)
    if llm_type== "reasoning":
        return ChatDeepSeek(**llm_conf)


if __name__ == "__main__":
    llm = get_llm_by_type("basic")
    print(llm)