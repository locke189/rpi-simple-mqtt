#import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from gpiozero import LED
import os 
import logging
import time
import argparse
import json

#CERT STUFF
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_CA_PATH = ROOT_PATH + "/certs/root-CA.crt"
DEVICE_CA_PATH = ROOT_PATH + "/certs/RPI-DeathRay.cert.pem"
PRIVATE_KEY_PATH = ROOT_PATH + "/certs/RPI-DeathRay.private.key"

#MQTT CLIENT CONFIG
CLIENT_ID = "basicPubSub"
HOST = "a1195qphodhbi1-ats.iot.us-east-1.amazonaws.com"
PORT = 8883
TOPIC = "devices/1"

led = LED(19)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("devices/1", 0)
    client.publish(topic="devices/1", payload="device-off")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == 'devices/1' and str(msg.payload.decode("utf-8")) == 'toggle':
      if led.value == 1:
          print("on")
          led.off()
          client.publish(topic="devices/1", payload="device-off")
      else:
          print("off")
          led.on()
          client.publish(topic="devices/1", payload="device-on")

led.off()
client = None
client = AWSIoTMQTTClient(CLIENT_ID, useWebsocket=False)
client.configureEndpoint(HOST, PORT)
client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, DEVICE_CA_PATH)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

#client.on_connect = on_connect
#client.on_message = on_message

# client.onMessage = on_message
# client.onOnline = on_connect

print('connecting')
client.connect()
client.subscribe(topic, 1, on_message)
time.sleep(2)
print('subscribing')
# client.publish(topic="devices/1", payload="device-on")
print('last')
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
loopCount = 0
while True:
    message = {}
    message['message'] = 'hello world'
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    client.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)