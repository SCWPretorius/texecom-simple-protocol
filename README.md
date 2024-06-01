# Texecom Simple Protocol

This is a Python-based project that interacts with an alarm system. It establishes a connection, 
authenticates with the alarm, reads from the stream, identifies the panel, and reads the LCD text and zone status periodically.

It is built and tested for the Texecom Premier 832 alarm panel. It should work for other Texecom panels such as the Premier 412 and Premier 816.

## Notice
I am busy rewriting my testing code into this repository with a bit more structure.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python
- pip

### Installing

Clone the repository to your local machine:

```bash
git clone https://github.com/SCWPretorius/texecom-simple-protocol.git
```

Navigate to the project directory:

```bash
cd texecom-simple-protocol
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command:

```bash
python app.py
```

## Project Structure

The project has several Python scripts:

- `app.py`: The main application script.
- `commands.py`: Contains a function to send a command to a given connection.
- `lcd_text.py`: Contains a function to read the LCD text periodically.
- `send_command_queue.py`: Contains functions to send commands to a queue and read commands from a queue.
- `connection.py`: Contains functions to create and close a connection.
- `authentication.py`: Contains a function to authenticate with the alarm.
- `panel.py`: Contains a function to identify the panel.
- `reader.py`: Contains a function to read from the stream.
- `zone_status.py`: Contains a function to read the zone status periodically.

##  Notice

This project was built through reverse engineering and debugging the alarm panel using the serial connection. 
It has also utilized resources from the following GitHub repositories:

- [pialarm](https://github.com/shuckc/pialarm/blob/master/protocol/wintex-protocol.md)
- [TexecomVeraPlugin](https://github.com/Samyoue/TexecomVeraPlugin/blob/master/L_Texecom.lua)

Please note that the use of these resources is for educational and development purposes only. 
The developers of this project do not endorse or encourage any form of illegal activity related to the use of this code. 
It is the user's responsibility to comply with all applicable laws and regulations when using this software.

This project is licensed under the MIT License.
