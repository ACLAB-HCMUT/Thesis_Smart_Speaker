import json
import time
import paho.mqtt.client as mqtt


BROKER = "app.coreiot.io" 
PORT = 1883
ACCESS_TOKEN = "DNBAxQJK7iZ0FP8eltCp"  


ATTRIBUTES_TOPIC_PUB = "v1/devices/me/attributes"
ATTRIBUTES_TOPIC_SUB = "v1/devices/me/attributes/response/+"
ATTRIBUTES_REQUEST_TOPIC = "v1/devices/me/attributes/request/1"

# json mau 
shared_data = {
    "device_name": "Pi_001",
    "status": "online",
    "config": {
        "mode": "auto",
        "threshold": 75
    }
}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
 
    client.subscribe(ATTRIBUTES_TOPIC_SUB)
 
    client.publish(ATTRIBUTES_REQUEST_TOPIC, "")


def on_message(client, userdata, msg):
    print("Received message from topic:", msg.topic)
    payload = json.loads(msg.payload.decode())
    print("Shared Attributes Update:", json.dumps(payload, indent=2))

   
    if "config" in payload:
        config = payload["config"]
        print(">> Đã nhận lệnh cấu hình mới:")
        print(f">> Mode: {config.get('mode')}, Threshold: {config.get('threshold')}")


client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.on_connect = on_connect
client.on_message = on_message

# connect
client.connect(BROKER, PORT, 60)

# send
def update_shared_attributes():
    client.publish(ATTRIBUTES_TOPIC_PUB, json.dumps(shared_data))
    print("Đã gửi dữ liệu lên Shared Attributes.")


client.loop_start()
update_shared_attributes()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    print("Ngắt kết nối.")
    client.loop_stop()
    client.disconnect()
