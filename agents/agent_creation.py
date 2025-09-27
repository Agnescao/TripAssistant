from langgraph.prebuilt import create_react_agent

from llm.llm_provider import get_llm_by_type


#create agents based on configured model and prompts
def create_agents(agent_name:str, agent_type:str,tools:list,prompt_template:str):
    """Factory function to create agents based on type."""
    return create_react_agent(
        name=agent_name,
        model=get_llm_by_type(agent_type),
        tools=tools,
        prompt_template=prompt_template,
    )