from commands import send_command
from config import udl_passcode

def authenticate_with_alarm(conn):
    """
    This function authenticates with the alarm system by sending a command with the UDL passcode.
    :param conn: The connection to which the command is to be sent.
    """
    command = f"\\W{udl_passcode}/"
    send_command(conn, command)
