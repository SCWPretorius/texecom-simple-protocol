import time
from commands import send_command


def read_zone_status_periodically(conn):
    """
    This function reads the zone status periodically every 1 second.
    :param conn: The connection from which the zone status is to be read.
    """
    while True:
        zone_status(conn)
        time.sleep(1)


def zone_status(conn):
    """
    This function sends a command to read the zone status from the given connection.
    :param conn: The connection to which the command is to be sent.
    """
    start_zone = 0x00
    num_zones = 0x11
    command = f"\\Z{chr(start_zone)}{chr(num_zones)}/"
    send_command(conn, command)
