import paho.mqtt.client as mqtt
from config import mqtt_broker_ip, mqtt_broker_port, mqtt_username, mqtt_password

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message

        # Set the username and password
        self.client.username_pw_set(username=mqtt_username, password=mqtt_password)

        self.client.connect(mqtt_broker_ip, mqtt_broker_port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {str(rc)}")
        client.subscribe("your/topic")  # Subscribe to a topic

    def on_publish(self, client, userdata, mid):
          print("Message Published...")

    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode()} on topic {message.topic}")

    def publish_to_home_assistant(self, topic, payload):
        try:
            # Publish a message
            self.client.publish(topic, payload)

            # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
            self.client.loop_start()
        except Exception as e:
            print(f"Failed to publish message: {e}")
