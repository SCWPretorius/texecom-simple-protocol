import socket
import logging
from config import address, port

def create_connection():
    """
    This function creates a connection to the server using the address and port specified in the config file.
    If the connection is successful, it logs that the server is connected and returns the connection object.
    If an error occurs during the connection, it logs the error and returns None.
    :return: The connection object if successful, or None if an error occurred.
    """
    try:
        conn = socket.create_connection((address, port))
        logging.info("Connected to server.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to server: {e}")
        return None


def close_connection(conn):
    """
    This function closes the given connection.
    :param conn: The connection to be closed.
    """
    conn.close()
