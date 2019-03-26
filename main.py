import paho.mqtt.client as mqtt
from time import sleep
from gpiozero import LED

led = LED(19)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("devices/1")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == 'devices/1':
      if led.value == 1:
          print("on")
          led.off()
          mqtt.publish.single("devices/1", "device-off", retain=True)
      else:
          print("off")
          led.on()
          mqtt.publish.single("devices/1", "device-on", retain=True)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.51", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()