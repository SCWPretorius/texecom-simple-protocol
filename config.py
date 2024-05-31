import logging
import os
from dotenv import load_dotenv

load_dotenv()

"""
This module is used for configuration settings. It loads environment variables from a .env file using the dotenv module.

The environment variables include:
- ADDRESS: The address of the server to connect to.
- PORT: The port of the server to connect to.
- UDL_PASSCODE: The passcode for UDL.
- LOGGING_LEVEL: The level of logging to use.

The module also sets up basic logging configuration with the specified logging level.
"""

address = os.getenv("ADDRESS")
port = os.getenv("PORT")
udl_passcode = os.getenv("UDL_PASSCODE")
logging_level = os.getenv("LOGGING_LEVEL")
mqtt_broker_ip = os.getenv("MQTT_BROKER_IP")
mqtt_broker_port = os.getenv("MQTT_BROKER_PORT")
mqtt_username = os.getenv("MQTT_USERNAME")
mqtt_password = os.getenv("MQTT_PASSWORD")

number_of_zones = None
try:
    number_of_zones = int(os.getenv("NUMBER_OF_ZONES"))
except ValueError:
    logging.error("NUMBER_OF_ZONES must be an integer.")
    number_of_zones = None  # or a default value

logging.basicConfig(level=logging_level)
