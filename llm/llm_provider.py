from langchain_core.language_models import BaseChatModel


def get_llm_by_type(llm_type: str) -> BaseChatModel:
    """
    Get LLM instance by type. Returns cached instance if available.
    """

    return None