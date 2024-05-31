from commands import send_command


def panel_identification(conn):
    """
    This function sends a panel identification command to the given connection.
    :param conn: The connection to which the command is to be sent.
    """
    command = "\\I/"
    send_command(conn, command)
