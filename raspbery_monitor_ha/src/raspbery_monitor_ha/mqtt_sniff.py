import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("CONNECTED", rc)
    client.subscribe("#")

def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload.decode(errors='ignore')}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.230", 1883, 60)
client.loop_forever()