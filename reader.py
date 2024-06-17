import binascii
import json
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
        # Split the hex message by '0d0a' and process each response separately
        responses = hex_message.split('0d0a')
        decoded_responses = []
        """
        The zone status is returning the status of 17 zone for me as the following when all zones are closed:
        00000000000000000000000000000000000d0a
        the code below is to split the hex message into 2 characters each and remove the last 4 characters
        ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
        if a zone is open the zone will read 01 instead of 00
        we need a better way of identifying this zone status, but for now it does the job
        """
        for response in responses:
            # Split the response into 2 characters each
            response_split = [response[i:i + 2] for i in range(0, len(response), 2)]

            if len(response_split) == number_of_zones:
                decoded_responses.append(response_split)
            else:
                ascii_string = binascii.unhexlify(response).decode().strip()
                decoded_responses.append(ascii_string)

        return decoded_responses
    except binascii.Error as e:
        logging.error(f"Error decoding hex message: {e}")
        return None


def process_partition_armed_response(ascii_string, mqtt_client):
    """
    This function checks if the ASCII string starts with "AREA ARMED". If it does, it finds the position of ">",
    extracts the part of the string after ">", and creates a dictionary from the characters.

    :param ascii_string: The ASCII string to be processed.
    """
    index = ascii_string.find(">")
    if index != -1:
        response = ascii_string[index + 1:index + 5]
        response_dict = {f"partition_{i + 1}": '0' if char == '.' else '1' for i, char in enumerate(response)}

        for partition, status in response_dict.items():
            topic = f"homeassistant/binary_sensor/texecom_alarm/{partition}_status"
            payload = {
                "partition_status": "OFF" if status == '0' else "ON",
                "device": {
                    "identifiers": "alarm_panel",
                    "name": "Texecom Premier",
                    "manufacturer": "Texecom",
                    "model": "Premier 832"
                },
                "qos": 0,
                "retain": True
            }
            mqtt_client.publish_to_home_assistant(topic, json.dumps(payload))
    else:
        logging.info(f"Received an AREA ARMED response without '>': {ascii_string}")


def process_known_response(ascii_string, mqtt_client):
    """
    This function checks if the ASCII string is a known response. If it is, it logs the response type.

    :param ascii_string: The ASCII string to be checked.
    """
    response_type = KNOWN_RESPONSES.get(ascii_string)
    if response_type == "Panel Identification":
        formatted_panel_id = ascii_string.replace("V", " V")
        payload = {
            "model": formatted_panel_id,
            "device": {
                "identifiers": "alarm_panel",
                "name": "Texecom Premier",
                "manufacturer": "Texecom",
                "model": "Premier 832"
            },
            "qos": 0,
            "retain": True
        }

        mqtt_client.publish_to_home_assistant("homeassistant/sensor/texecom_alarm/panel_model", json.dumps(payload))
        logging.info(f"Received a {response_type} response: {ascii_string}")
    elif response_type:
        logging.info(f"Received a {response_type} response: {ascii_string}")
    else:
        logging.info(f"Received an unknown response: {ascii_string}")


def process_zone_status_response(zone_array, mqtt_client):
    for index, zone in enumerate(zone_array):
        topic = f"homeassistant/binary_sensor/texecom_alarm/zone_{index + 1}"
        payload = {
            "zone_status": "OFF" if zone == '00' else "ON",
            "device": {
                "identifiers": "alarm_panel",
                "name": "Texecom Premier",
                "manufacturer": "Texecom",
                "model": "Premier 832"
            },
            "qos": 0,
            "retain": True
        }
        mqtt_client.publish_to_home_assistant(topic, json.dumps(payload))


def read_stream(conn, mqtt_client):
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

            responses = decode_message(data)
            for response in responses:
                if isinstance(response, list):
                    process_zone_status_response(response, mqtt_client)
                elif response.startswith("AREA ARMED"):
                    process_partition_armed_response(response, mqtt_client)
                # elif response:
                #     process_known_response(response, mqtt_client)
    except Exception as e:
        logging.error(f"Error reading from connection: {e}")
