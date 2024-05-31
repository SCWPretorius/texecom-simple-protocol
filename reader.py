import binascii
import logging

from config import number_of_zones
from known_responses import KNOWN_RESPONSES


def decode_message(data):
    """
    This function takes in raw data, converts it to a hexadecimal string, and then to an ASCII string.
    If an error occurs during this process, it is logged and None is returned.

    :param data: The raw data to be decoded.
    :return: The decoded ASCII string, or None if an error occurred.
    """
    try:
        hex_message = binascii.hexlify(data).decode()

        """
        The zone status is returning the status of 17 zone for me as the following when all zones are closed:
        00000000000000000000000000000000000d0a
        the code below is to split the hex message into 2 characters each and remove the last 4 characters
        ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
        if a zone is open the zone will read 01 instead of 00
        we need a better way of identifying this zone status, but for now it does the job
        """
        hex_message_split = [hex_message[i:i + 2] for i in range(0, len(hex_message), 2)]
        hex_message_split = hex_message_split[:-2]
        if len(hex_message_split) == number_of_zones:
            return hex_message_split

        ascii_string = binascii.unhexlify(hex_message).decode().strip()
        return ascii_string
    except binascii.Error as e:
        logging.error(f"Error decoding hex message: {e}")
        return None


def process_area_armed_response(ascii_string):
    """
    This function checks if the ASCII string starts with "AREA ARMED". If it does, it finds the position of ">",
    extracts the part of the string after ">", and creates a dictionary from the characters.

    :param ascii_string: The ASCII string to be processed.
    """
    if ascii_string.startswith("AREA ARMED"):
        index = ascii_string.find(">")
        if index != -1:
            response = ascii_string[index + 1:index + 5]
            response_dict = {f"area{i + 1}": char for i, char in enumerate(response)}
            logging.info(f"Received an AREA ARMED response: {response} - {response_dict}")
        else:
            logging.info(f"Received an AREA ARMED response without '>': {ascii_string}")


def process_known_response(ascii_string):
    """
    This function checks if the ASCII string is a known response. If it is, it logs the response type.

    :param ascii_string: The ASCII string to be checked.
    """
    response_type = KNOWN_RESPONSES.get(ascii_string)
    if response_type:
        logging.info(f"Received a {response_type} response: {ascii_string}")
    else:
        logging.info(f"Received an unknown response: {ascii_string}")


def process_zone_status_response(zone_array):
    zone_dict = {f"zone_{i + 1}": zone_array[i] for i in range(len(zone_array))}
    logging.info(f"Received a zone status response: {zone_dict}")


def read_stream(conn):
    """
    This function reads data from a connection in a loop. For each chunk of data, it decodes the message,
    processes the "AREA ARMED" response, and processes known responses.

    :param conn: The connection to read from.
    """
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            response = decode_message(data)
            if isinstance(response, list):
                process_zone_status_response(response)
            elif response:
                process_area_armed_response(response)
                process_known_response(response)
    except Exception as e:
        logging.error(f"Error reading from connection: {e}")
