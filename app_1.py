import os
import socket
import threading
import time
import logging
import binascii
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)


def authenticate_with_alarm(conn, udl_passcode):
    command = f"\\W{udl_passcode}/"
    try:
        conn.sendall(command.encode())
    except Exception as e:
        logging.error(f"Failed to write to connection: {e}")


def read_panel_identification(conn):
    command = "\\I/"
    try:
        conn.sendall(command.encode())
    except Exception as e:
        logging.error(f"Error writing to connection: {e}")


def read_lcd_text(conn):
    command = "\\L/"
    try:
        conn.sendall(command.encode())
    except Exception as e:
        logging.error(f"Error writing to connection: {e}")


def read_stream(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            # Print the raw byte array
            logging.info(f"Response (raw bytes): {data}")

            # Convert the raw message to a hexadecimal string for readability
            hex_message = binascii.hexlify(data).decode()

            # Print the hex representation of the message
            logging.info(f"Response (hex): {hex_message}")

            try:
                bytes_data = binascii.unhexlify(hex_message)
                logging.info(f"ASCII string: {bytes_data.decode()}")
            except binascii.Error as e:
                logging.error(f"Error decoding hex message: {e}")
    except Exception as e:
        logging.error(f"Error reading from connection: {e}")


def read_zone_status_periodically(conn):
    while True:
        read_zone_status(conn)
        time.sleep(1)


def read_zone_status(conn):
    start_zone = 0x00
    num_zones = 0x11
    command = f"\\Z{chr(start_zone)}{chr(num_zones)}/"

    try:
        conn.sendall(command.encode())
    except Exception as e:
        logging.error(f"Error writing to connection: {e}")


def main():
    address = os.getenv("ADDRESS")
    port = os.getenv("PORT")
    udl_passcode = os.getenv("UDL_PASSCODE")

    try:
        conn = socket.create_connection((address, port))
    except Exception as e:
        logging.error(f"Failed to connect to server: {e}")
        return

    authenticate_with_alarm(conn, udl_passcode)

    stream_thread = threading.Thread(target=read_stream, args=(conn,))
    stream_thread.daemon = True
    stream_thread.start()

    time.sleep(5)  # sleep for a few seconds to allow the panel to authenticate the connection

    read_panel_identification(conn)
    time.sleep(2)
    read_lcd_text(conn)

    zone_status_thread = threading.Thread(target=read_zone_status_periodically, args=(conn,))
    zone_status_thread.daemon = True
    zone_status_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
