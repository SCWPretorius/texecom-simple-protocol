import time
from commands import send_command

def read_lcd_text_periodically(conn):
    """
    This function reads the LCD text periodically every 5 seconds.
    :param conn: The connection from which the LCD text is to be read.
    """
    while True:
        lcd_text(conn)
        time.sleep(5)

def lcd_text(conn):
    """
    This function sends a command to read the LCD text from the given connection.
    :param conn: The connection to which the command is to be sent.
    """
    command = "\\L/"
    send_command(conn, command)
