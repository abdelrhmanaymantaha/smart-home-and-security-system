import paho.mqtt.client as paho
from paho import mqtt
import ssl
import json
import time


class MQTTSender:
    def __init__(self, broker, port, topic, username=None, password=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        # Use MQTTv5 for secure connection
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        # Enable TLS for secure connection
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

        # Set username and password if provided
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"CONNACK received with code {rc}.")

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def send_message(self, message):
        try:
            # Ensure the message is a string
            if not isinstance(message, str):
                message = str(message)
            # Publish the message
            self.client.publish(self.topic, message, qos=1)
            print(f"Message '{message}' published to topic '{self.topic}'")
        except Exception as e:
            print(f"An error occurred: {e}")

def mqtt_send(message: str, topic: str):
    mqtt_sender = MQTTSender(
        broker="2510b2ca3c0d421d82a56d56fa9e2f08.s1.eu.hivemq.cloud",
        port=8883,
        topic=topic,
        username='project',
        password='project123P'
    )
    mqtt_sender.client.connect(mqtt_sender.broker, mqtt_sender.port)
    mqtt_sender.client.loop_start()
    time.sleep(2)  # Wait for connection
    mqtt_sender.send_message(message)
    time.sleep(1)  # Give time for publish
    mqtt_sender.client.loop_stop()
    mqtt_sender.client.disconnect()


if __name__ == "__main__":
    # Example 1: Send 'ON' to the lamp topic
    mqtt_send('ON', topic='home/living room/lamp')

    # Example 2: Send '25' to the temperature topic
    mqtt_send('25', topic='home/living room/temperature')

    # Example 3: Send '200' to the fan topic
    mqtt_send('200', topic='home/living room/fan')