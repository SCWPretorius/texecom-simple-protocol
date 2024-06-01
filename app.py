import queue
import threading
import time
import logging

from connection import create_connection, close_connection
from authentication import authenticate_with_alarm
from lcd_text import read_lcd_text_periodically
from panel import panel_identification
from partition_output import partition_output
from reader import read_stream
from send_command_queue import send_commands_from_queue
from zone_status import read_zone_status_periodically

# Create a queue
command_queue = queue.Queue(maxsize=100)

def main():
    """
    This is the main function of the application. It establishes a connection, authenticates with the alarm,
    starts a thread to read from the stream, sleeps for a few seconds to allow the panel to authenticate the connection,
    identifies the panel, starts a thread to read the LCD text periodically, and then enters an infinite loop where it sleeps for 1 second at a time.
    If a KeyboardInterrupt is raised, it logs that the application is shutting down and then closes the connection.

    This function does not take any parameters and does not return anything.
    """
    conn = create_connection()
    if conn is None:
        return

    authenticate_with_alarm(conn)

    stream_thread = threading.Thread(target=read_stream, args=(conn,))
    stream_thread.daemon = True
    stream_thread.start()

    command_sender_thread = threading.Thread(target=send_commands_from_queue, args=(conn, command_queue))
    command_sender_thread.daemon = True
    command_sender_thread.start()

    time.sleep(5)  # sleep for a few seconds to allow the panel to authenticate the connection

    # Add other functionalities here
    panel_identification(conn)

    # partition_output(conn)

    """NOTE: The following is commented out because trying to focus on zones first"""
    # lcd_text_thread = threading.Thread(target=read_lcd_text_periodically, args=(conn, command_queue,))
    # lcd_text_thread.daemon = True
    # lcd_text_thread.start()

    zone_status_thread = threading.Thread(target=read_zone_status_periodically, args=(conn, command_queue,))
    zone_status_thread.daemon = True
    zone_status_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down.")
    finally:
        close_connection(conn)


if __name__ == "__main__":
    main()
