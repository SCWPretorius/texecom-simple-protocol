import logging

def send_command(conn, command):
    """
    This function sends a command to the given connection.
    :param conn: The connection to which the command is to be sent.
    :param command: The command to be sent.
    """
    try:
        conn.sendall(command.encode())
    except Exception as e:
        logging.error(f"Failed to write to connection: {e}")
