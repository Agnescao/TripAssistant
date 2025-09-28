from langchain_core.runnables import RunnableConfig
from typing import Optional, List, Dict, Any

def fetch_flight_info(config: RunnableConfig) -> List[Dict]:
    """
    Fetch flight information based on the provided configuration.

    Args:
        config (RunnableConfig): Configuration containing flight search parameters.

    Returns:
        List[Dict]: A list of dictionaries containing flight details.
    """
    import requests
    from typing import List, Dict

    api_key = config

