import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import serial
import time

mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "velocity"
port = 1883

# XBee setting

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, baudrate = 9600)

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)

i = 0
while True:
    # send RPC to remote

    s.write("/getAcc/run\r".encode())
    i+=1
    if i >= 5:
        mesg=s.readline()
        mqttc.publish(topic, mesg)
        print(mesg)
    time.sleep(1)
        
s.close()
