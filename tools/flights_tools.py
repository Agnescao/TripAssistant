from datetime import date, datetime


import pytz
from langchain_core.runnables import RunnableConfig
from typing import Optional, List, Dict, Any

from langchain_core.tools import tool

from tools.dbconnection import dbconnection

@tool
def fetch_flight_info(config: RunnableConfig) -> List[Dict]:
    """
     fetch flight information based on user id.


    :param config:
    :return: dict with flight deatails
    """

    configuration = config.get('configurable', {})
    passenger_id = configuration.get('passenger_id', None)
    if not passenger_id:
        raise ValueError("Passenger ID is required.")

    db_conn = dbconnection()
    conn = db_conn.connection
    cursor = db_conn.cursor

    # sql query join tickets and passengers  table to get flight details
    query = """
      SELECT 
         t.ticket_no, t.book_ref,
         f.flight_id, f.flight_no, f.departure_airport, f.arrival_airport, f.scheduled_departure, f.scheduled_arrival,
         bp.seat_no, tf.fare_conditions
     FROM 
         tickets t
         JOIN ticket_flights tf ON t.ticket_no = tf.ticket_no
         JOIN flights f ON tf.flight_id = f.flight_id
         JOIN boarding_passes bp ON bp.ticket_no = t.ticket_no AND bp.flight_id = f.flight_id
     WHERE 
         t.passenger_id = ?
     """
    cursor.execute(query, (passenger_id,))
    print("Executing query to fetch flight information for passenger_id:", passenger_id)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]

    results = [dict(zip(column_names, row)) for row in rows] # convert rows to dict
    cursor.close()
    conn.close()

    return results



@tool
def search_flight_info(departure_airport:Optional[str], arrival_airport:Optional[str], departure_date:Optional[date | datetime], arrival_date:Optional[date | datetime],limit:int =20) -> List[Dict]:
    """
     search flight information based on user input.


    :param
     departure_airport: shengzhen airport
     arrival_airport: shanghai airport
     departure_date: 2024-10-10
     arrival_date: 2024-10-11
     limit: number of results to return
    :return: dict with flight details
    """

    db_conn = dbconnection()
    conn = db_conn.connection
    cursor = db_conn.cursor

    query = "select * from flights where 1=1"
    params=[]
    if departure_airport:
        query += " and departure_airport=?"
        params.append(departure_airport)
    if arrival_airport:
        query += " and arrival_airport=?"
        params.append(arrival_airport)
    if departure_date:
        query += " and scheduled_departure>=?"
        params.append(departure_date)
    if arrival_date:
        query += " and scheduled_arrival<=?"
        params.append(arrival_date)
    query += " limit ?"
    params.append(limit)
    cursor.execute(query, params)
    print("Executing query to search flight information:", query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return results


@tool
def update_flight_info(ticket_no:str, new_flight_id:str, config:RunnableConfig) -> str:
    """
     update flight information based on user input.


    :param
     ticket_no: ticket number
     flight_id: new flight id
     config: RunnableConfig with passenger_id
    :return: str with update status
    """

    configuration = config.get('configurable', {})
    passenger_id = configuration.get('passenger_id', None)
    if not passenger_id:
        raise ValueError("Passenger ID is required.")

    db_conn = dbconnection()
    conn = db_conn.connection
    cursor = db_conn.cursor

    # check if the ticket belongs to the passenger
    query = "select * from tickets where ticket_no=? and passenger_id=?"
    cursor.execute(query, (ticket_no, passenger_id))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return f"Ticket {ticket_no} does not belong to passenger {passenger_id}."

    # check if the new flight exists
    query = "select * from flights where flight_id=?"
    cursor.execute(query, (new_flight_id,))
    new_flight = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return f"Flight {new_flight_id} does not exist."

    column_names = [column[0] for column in cursor.description]
    new_flight_dict = dict(zip(column_names, new_flight))
    # set timezone and calculate the difference between arrial time and current time

    timezone = pytz.timezone("Asia/Shanghai")
    current_time=datetime.now(timezone)
    departure_time = datetime.strptime(new_flight_dict["scheduled_departure"], "%Y-%m-%d %H:%M:%S")
    time_until_departure = (departure_time - current_time).total_seconds()
    if time_until_departure <(1*3600):
        return f"The flight {new_flight_id} is too close to departure time."

    # check if the user already has a ticket for the new flight
    query = "select * from ticket_flights where ticket_no=? and flight_id=?"
    cursor.execute(query, (ticket_no, new_flight_id))
    existing_ticket = cursor.fetchone()
    if existing_ticket:
        cursor.close()
        conn.close()
        return f"Passenger {passenger_id} already has a ticket for flight {new_flight_id}."


    # update the flight id in ticket_flights table
    update_query = "update ticket_flights set flight_id=? where ticket_no=?"
    cursor.execute(update_query, (new_flight_id, ticket_no))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Ticket {ticket_no} has been updated to flight {new_flight_id}."


@ tool

def cancel_flight(ticket_no:str, config:RunnableConfig) -> str:
    """
     cancel flight based on user input.


    :param
     ticket_no: ticket number
     config: RunnableConfig with passenger_id
    :return: str with cancel status
    """
    configuration = config.get('configurable', {})
    passenger_id = configuration.get('passenger_id', None)
    if not passenger_id:
        raise ValueError("Passenger ID is required.")

    db_conn = dbconnection()
    conn = db_conn.connection
    cursor = db_conn.cursor
    # check if the ticket belongs to the passenger
    query = "select * from tickets where ticket_no=? and passenger_id=?"
    cursor.execute(query, (ticket_no, passenger_id))
    existing_ticket = cursor.fetchone()
    if not existing_ticket:
        cursor.close()
        conn.close()
        return f"Ticket {ticket_no} does not belong to passenger {passenger_id}."


    # check if the flight has already been cancelled
    query = "select * from ticket_flights where ticket_no=? and status='C'"
    cursor.execute(query, (ticket_no,))
    cancelled_ticket = cursor.fetchone()
    if cancelled_ticket:
        cursor.close()
        conn.close()
        return f"Ticket {ticket_no} has already been cancelled."

    # cancel the flight
    update_query = "update ticket_flights set status='C' where ticket_no=?"
    cursor.execute(update_query, (ticket_no,))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Ticket {ticket_no} has been cancelled."

