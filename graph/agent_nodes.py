# Handoffs
from typing import Annotated
import os

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.graph import MessagesState
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from agents.agent_creation import create_agents
from tools.search_tool import WebSearchTool
from tools.confirmation_tool import generic_confirmation


def create_handoff_tool(agent_name, description):
    """Create a handoff tool for delegating tasks to another agent.
    Args:
        agent_name (str): The name of the agent to which the task will be delegated.
        description (str): A brief description of the tool's purpose.
    Returns:
        function: A tool function that can be used to delegate tasks.

    """
    name = f"assign_to_{agent_name}"
    description = description or f"ask {agent_name} for help"

    @tool(name, description=description)
    def assign_to_agent(state:Annotated[MessagesState,InjectedState],tool_call_id:Annotated[str,InjectedToolCallId]) -> Command:
        """Assign a task to another agent.
        Args:
            state (MessagesState): The current state containing messages.
            tool_call_id (str): The ID of the tool call containing the task to be assigned.

        Returns:
            Command: A command indicating the task has been assigned.
        """

        # create tool message to record the task
        tool_message = {
            "role": "tool",
            "content": f"Delegating task to {agent_name}.",
            "tool_call_id": tool_call_id,
            "name": name,
        }
        # return command to assign the task with target agent
        return Command(
            goto=agent_name,
            graph=Command.PARENT,
            update={**state, "messages": state["messages"]+[tool_message]}
        )
    return assign_to_agent


assign_to_research_agent = create_handoff_tool(
    agent_name="research_agent",
    description="将任务分配给：research_agent智能体。",
)

assign_to_flight_booking_agent = create_handoff_tool(
    agent_name="flight_booking_agent",
    description="将任务分配给：flight_booking_agent智能体。",
)
assign_to_hotel_booking_agent = create_handoff_tool(
    agent_name="hotel_booking_agent",
    description="将任务分配给：hotel_booking_agent智能体。",
)
assign_to_car_rental_booking_agent = create_handoff_tool(
    agent_name="car_rental_booking_agent",
    description="将任务分配给：car_rental_booking_agent智能体。",
)
assign_to_excursion_booking_agent = create_handoff_tool(
    agent_name="excursion_booking_agent",
    description="将任务分配给：excursion_booking_agent智能体。",
)


def get_prompt_template(prompt_name):
    """get the prompt template by name by read markdown file
       Args:
           prompt_name (str): the name of the prompt template
       Returns:
           str: the content of the prompt template
           
       example : prompt/supervisor.md
    """
    # 使用绝对路径或相对于当前文件的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "..", "prompt", prompt_name + ".md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

research_agent = create_agents("research_agent", "basic", [WebSearchTool()], get_prompt_template("research"))
flight_booking_agent = create_agents("flight_booking_agent", "basic", [generic_confirmation], get_prompt_template("flight_booking"))
hotel_booking_agent = create_agents("hotel_booking_agent", "basic", [generic_confirmation], get_prompt_template("hotel_booking"))
car_rental_booking_agent = create_agents("car_rental_booking_agent", "basic", [generic_confirmation], get_prompt_template("car_rental_booking"))
excursion_booking_agent = create_agents("excursion_booking_agent", "basic", [generic_confirmation], get_prompt_template("excursion_booking"))
recommendation_agent = create_agents("recommendation_agent", "basic", [generic_confirmation], get_prompt_template("recommendation"))
train_booking_agent = create_agents("train_booking_agent", "basic", [generic_confirmation], get_prompt_template("train_booking"))


supervisor_agent = create_agents("supervisor_agent", "basic", [assign_to_research_agent, assign_to_flight_booking_agent, assign_to_hotel_booking_agent, assign_to_car_rental_booking_agent, assign_to_excursion_booking_agent], get_prompt_template("supervisor"))