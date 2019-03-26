#import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as mqtt
from time import sleep
from gpiozero import LED
import os 

#CERT STUFF
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_CA_PATH = ROOT_PATH + "/certs/AmazonRootCA1.cert.pem"
DEVICE_CA_PATH = ROOT_PATH + "/certs/RPI-DeathRay.cert.pem"
PRIVATE_KEY_PATH = ROOT_PATH + "/certs/RPI-DeathRay.private.key"
PUBLIC_KEY_PATH = ROOT_PATH + "/certs/RPI-DeathRay.public.key"

#MQTT CLIENT CONFIG
CLIENT_ID = "DEATH_RAY_00"
HOST = "a1195qphodhbi1-ats.iot.us-east-1.amazonaws.com"
PORT = 8883

led = LED(19)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("devices/1", 0)
    client.publish(topic="devices/1", payload="device-off", 0)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == 'devices/1' and str(msg.payload.decode("utf-8")) == 'toggle':
      if led.value == 1:
          print("on")
          led.off()
          client.publish(topic="devices/1", payload="device-off", 0)
      else:
          print("off")
          led.on()
          client.publish(topic="devices/1", payload="device-on", 0)

led.off()

client = mqtt(CLIENT_ID)
client.configureEndpoint("YOUR.ENDPOINT", 8883)
client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, DEVICE_CA_PATH)

client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

#client.on_connect = on_connect
#client.on_message = on_message

client.onMessage = on_message
client.onOnline = on_connect
client.connect()

client.subscribe()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()