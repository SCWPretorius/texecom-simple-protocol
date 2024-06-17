FROM python:3-alpine

WORKDIR /usr/src/app

COPY . .

ENV ADDRESS="0.0.0.0"
ENV PORT="10001"
ENV UDL_PASSCODE="1234"
ENV NUMBER_OF_ZONES=17
ENV MQTT_BROKER_IP="0.0.0.0"
ENV MQTT_BROKER_PORT="1883"
ENV MQTT_USERNAME="username"
ENV MQTT_PASSWORD="password"

RUN pip install paho-mqtt

CMD ["python", "app.py" ]
