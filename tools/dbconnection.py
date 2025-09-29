import sqlite3
from typing import Tuple


class DbConnection:
    def __init__(self, cursor: sqlite3.Cursor, connection: sqlite3.Connection) -> None:
        self.cursor = cursor
        self.connection = connection


def get_db_connection(database_path: str = "../travel.db") -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Create and return a database connection and cursor.
    
    Args:
        database_path (str): Path to the SQLite database file
        
    Returns:
        Tuple[sqlite3.Connection, sqlite3.Cursor]: Connection and cursor objects
    """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    return connection, cursor


def dbconnection(database_path: str = "../travel.db") -> DbConnection:
    """
    Create and return a DbConnection object.
    
    Args:
        database_path (str): Path to the SQLite database file
        
    Returns:
        DbConnection: Object containing cursor and connection
    """
    conn, cursor = get_db_connection(database_path)
    return DbConnection(cursor, conn)