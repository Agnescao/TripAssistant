from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState

from tools.flights_tools import fetch_flight_info


def format_flight_info(flight_data:list[dict]) -> list[str]:
    """Format flight information into a readable string."""
    if not flight_data:
        return "No flight information available."

    formatted_info = "Here are the available flights:\n"
    for flight in flight_data:
        formatted_info += (
            f"-------------------------\n"
            f"Your flight ticket details:\n"
            f"Ticket_id: {flight.get('ticket_id', 'N/A')}\n"
            f"Flight Number: {flight.get('flight_number', 'N/A')}\n"
            f"Departure: {flight.get('departure', 'N/A')} at {flight.get('departure_time', 'N/A')}\n"
            f"Arrival: {flight.get('arrival', 'N/A')} at {flight.get('arrival_time', 'N/A')}\n"
            f"Seat_no: {flight.get('seat_no', 'N/A')}\n"
            f"Fare_conditions: {flight.get('fare_conditions', 'N/A')}\n"
            f"Price: {flight.get('price', 'N/A')}\n"
            "-------------------------\n"
        )
    return formatted_info





def get_user_info(state: MessagesState, config: RunnableConfig):
    """
    Fetch user information based on the current state and configuration.
    :param state:
    :param config:
    :return: dit {"messages":} "fetch flight or train info"}
    """

    if "messages" in state:
        for message in state["messages"]:
            # if found flight or train info, return directly
            if isinstance(message,AIMessage) and message.id=='user_info_success':
                return

    flight_data = fetch_flight_info(config)
    if flight_data:
        flight_message=(AIMessage(content=format_flight_info(flight_data), id='user_info_success'))

    else:
        flight_message=(AIMessage(content="No flight information available.", id='user_info_failed'))

    """fetch train info as above"""
    train_data = fetch_train_info(config)
    return {
        "messages": [flight_message],  # 新增 AIMessage
    }