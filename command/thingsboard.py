import paho.mqtt.client as mqttclient
import json
import time

BROKER_ADDRESS = "app.coreiot.io"  
PORT = 1883  

def update_device_state(access_token, data):
    
    client = mqttclient.Client()
    client.username_pw_set(access_token)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Kết nối thành công tới ThingsBoard")
            payload = json.dumps(data)
            client.publish("v1/devices/me/attributes", payload, 1)
            print(f"Dữ liệu đã gửi: {payload}")
            time.sleep(1)  
            client.disconnect()
        else:
            print(f" Kết nối thất bại với mã lỗi {rc}")

    client.on_connect = on_connect
    client.connect(BROKER_ADDRESS, PORT)
    client.loop_start()
    time.sleep(2) 

# ACCESS_TOKEN = "6e2vlzqcf3ci6cd2p8n3"
ACCESS_TOKEN = "ozu62mz72ssdznrcqvhy"

update_device_state(ACCESS_TOKEN, {"device_state": 1})  
# update_device_state(ACCESS_TOKEN, {"device_state": 0})  
