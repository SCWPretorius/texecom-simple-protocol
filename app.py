import json
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
from mqtt import MQTTClient

from config import number_of_zones

# Create a queue
command_queue = queue.Queue(maxsize=100)


def zone_discovery(mqtt_client):
    for index in range(number_of_zones):
        topic = f"homeassistant/binary_sensor/texecom_alarm/zone_{index + 1}"
        value_template = "{{ value_json.zone_status }}"
        name = f"Zone {index + 1}"
        unique_id = f"zone_{index + 1}"
        config_payload = {
            "name": name,
            "unique_id": unique_id,
            "state_topic": topic,
            "value_template": value_template,
            "device_class": "motion",
            "payload_on": "ON",
            "payload_off": "OFF",
            "device": {
                "identifiers": "alarm_panel",
                "name": "Texecom Premier",
                "manufacturer": "Texecom",
                "model": "Premier 832"
            },
            "qos": 0,
            "retain": True
        }

        config_topic = f"homeassistant/binary_sensor/texecom_alarm/zone_{index + 1}/config"
        mqtt_client.publish_to_home_assistant(config_topic, json.dumps(config_payload))


def panel_model_discovery(mqtt_client):
    json_message = {
        "name": "Alarm Model",
        "unique_id": "alarm_model",
        "entity_category": "diagnostic",
        "value_template": "{{ value_json.model }}",
        "state_topic": "homeassistant/sensor/texecom_alarm/panel_model",
        "device": {
            "identifiers": "alarm_panel",
            "name": "Texecom Premier",
            "manufacturer": "Texecom",
            "model": "Premier 832"
        },
        "qos": 0,
        "retain": True
    }

    mqtt_client.publish_to_home_assistant("homeassistant/sensor/texecom_alarm/config", json.dumps(json_message))


def partition_status_discovery(mqtt_client):
    for index in range(4):
        topic = f"homeassistant/sensor/texecom_alarm/partition_{index + 1}_status"
        value_template = "{{ value_json.partition_status }}"
        name = f"Partition {index + 1} Status"
        unique_id = f"partition_{index + 1}_status"
        config_payload = {
            "name": name,
            "unique_id": unique_id,
            "state_topic": topic,
            "value_template": value_template,
            "device": {
                "identifiers": "alarm_panel",
                "name": "Texecom Premier",
                "manufacturer": "Texecom",
                "model": "Premier 832"
            },
            "qos": 0,
            "retain": True
        }

        mqtt_client.publish_to_home_assistant(f"homeassistant/sensor/texecom_alarm/partition_{index + 1}_status/config", json.dumps(config_payload))


def auto_discovery(mqtt_client):
    zone_discovery(mqtt_client)
    panel_model_discovery(mqtt_client)
    partition_status_discovery(mqtt_client)


def main():
    """
    This is the main function of the application. It establishes a connection, authenticates with the alarm,
    starts a thread to read from the stream, sleeps for a few seconds to allow the panel to authenticate the connection,
    identifies the panel, starts a thread to read the LCD text periodically, and then enters an infinite loop where it sleeps for 1 second at a time.
    If a KeyboardInterrupt is raised, it logs that the application is shutting down and then closes the connection.

    This function does not take any parameters and does not return anything.
    """
    mqttClient = MQTTClient()

    auto_discovery(mqttClient)

    conn = create_connection()
    if conn is None:
        return

    authenticate_with_alarm(conn)

    stream_thread = threading.Thread(target=read_stream, args=(conn, mqttClient,))
    stream_thread.daemon = True
    stream_thread.start()

    command_sender_thread = threading.Thread(target=send_commands_from_queue, args=(conn, command_queue))
    command_sender_thread.daemon = True
    command_sender_thread.start()

    time.sleep(5)  # sleep for a few seconds to allow the panel to authenticate the connection

    # Add other functionalities here
    panel_identification(conn)

    # partition_output(conn)

    """NOTE: Using this, because having trouble with partition_output"""
    lcd_text_thread = threading.Thread(target=read_lcd_text_periodically, args=(conn, command_queue,))
    lcd_text_thread.daemon = True
    lcd_text_thread.start()

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
