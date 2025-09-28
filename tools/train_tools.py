from typing import List, Dict

from langchain_core.runnables import RunnableConfig

from mcp.train_mcp_client import internal_mcp_client


def fetch_train_info(config: RunnableConfig) -> List[Dict]:
    """
    Fetch train information based on the provided configuration.

    Args:
        config (RunnableConfig): Configuration containing train search parameters.

    Returns:
        List[Dict]: A list of dictionaries containing train information.
    """
    mcp_train_tools= internal_mcp_client.get_tools()
    print("fetched tool list:")
    for tool in mcp_train_tools:
        print(f"- {tool.name}")

    llm_with_tools = llm.bind_tools(mcp_train_tools)

    return llm_with_tools.invoke(config)
