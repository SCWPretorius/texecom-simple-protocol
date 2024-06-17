import time
from send_command_queue import send_command_to_queue


def read_zone_status_periodically(conn, command_queue):
    """
    This function reads the zone status periodically every 1 second.
    :param conn: The connection from which the zone status is to be read.
    """
    start_zone = 0x00
    num_zones = 0x11
    command = f"\\Z{chr(start_zone)}{chr(num_zones)}/"
    while True:
        send_command_to_queue(conn, command, command_queue)
        time.sleep(1)
