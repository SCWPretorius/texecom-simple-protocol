import logging


def send_command_to_queue(conn, command, command_queue):
    """
    This function puts a command into the queue.
    :param conn: The connection to which the command is to be sent.
    :param command: The command to be sent.
    :param command_queue: The queue to put the command into.
    """
    command_queue.put(command)

def send_commands_from_queue(conn, command_queue):
    """
    This function continuously reads from the queue and sends the commands to the connection.
    :param conn: The connection to send the commands to.
    :param command_queue: The queue to read the commands from.
    """
    while True:
        command = command_queue.get()
        try:
            conn.sendall(command.encode())
        except Exception as e:
            logging.error(f"Error writing to connection: {e}")
