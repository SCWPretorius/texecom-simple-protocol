# Texecom Alarm MQTT Interface

This project provides an interface between a Texecom alarm system and an MQTT broker. 
It is written in Python and uses the MQTT protocol to publish alarm status updates to a Home Assistant instance.

## Features

- Decodes messages from the Texecom alarm system.
- Processes "AREA ARMED" responses from keypad.
- Processes zone status responses.
- Publishes updates to Home Assistant via MQTT.

## Requirements

- Python 3.6 or higher
- An MQTT broker (e.g., Mosquitto)
- A Texecom Premier 832 alarm system

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/SCWPretorius/texecom-simple-protocol.git
```

Navigate to the project directory:

```bash
cd texecom-simple-protocol
```

## Usage

This application can be run using Docker. Here are the steps to do so:

1. Build the Docker image:
```bash
docker build -t texecom-simple-protocol .
```
2. Run the Docker container:
```bash
docker run -d --name texecom-simple-protocol texecom-simple-protocol
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project was built through reverse engineering and debugging the alarm panel using the serial connection. 
It has also utilized resources from the following GitHub repositories:

- [pialarm](https://github.com/shuckc/pialarm/blob/master/protocol/wintex-protocol.md)
- [TexecomVeraPlugin](https://github.com/Samyoue/TexecomVeraPlugin/blob/master/L_Texecom.lua)

Please note that the use of these resources is for educational and development purposes only. 
The developers of this project do not endorse or encourage any form of illegal activity related to the use of this code. 
It is the user's responsibility to comply with all applicable laws and regulations when using this software.

This project is licensed under the MIT License.
