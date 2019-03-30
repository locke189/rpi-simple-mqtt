import paho.mqtt.client as mqtt
import ssl
from time import sleep
from gpiozero import LED
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

host = 'm16.cloudmqtt.com'
port = 12844
user = 'qvuhxeov'
pwd = 'jDrhVb3FadZV'
led = LED(19)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("devices/1")
    client.publish(topic="devices/1", payload="device-off", retain=True)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == 'devices/1' and str(msg.payload.decode("utf-8")) == 'toggle':
      if led.value == 1:
          print("on")
          led.off()
          client.publish(topic="devices/1", payload="device-off", retain=True)
      else:
          print("off")
          led.on()
          client.publish(topic="devices/1", payload="device-on", retain=True)

led.off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# TLS

#client.tls_set(dir_path + "/m2mqtt_ca.crt", tls_version=ssl.PROTOCOL_TLSv1, cert_reqs=ssl.CERT_NONE)
#client.tls_insecure_set(True)
client.username_pw_set(username=user,password=pwd)
client.connect(host, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()