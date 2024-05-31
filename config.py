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
number_of_zones = os.getenv("NUMBER_OF_ZONES")

logging.basicConfig(level=logging_level)
