import time
from commands import send_command
from send_command_queue import send_command_to_queue


def read_lcd_text_periodically(conn, command_queue):
    command = "\\L/"
    while True:
        send_command_to_queue(conn, command, command_queue)
        time.sleep(5)


