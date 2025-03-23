import paho.mqtt.client as mqttclient
import json
import os
import time
from dotenv import load_dotenv


load_dotenv()
BROKER_ADDRESS = "app.coreiot.io" 
PORT = 1883  

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối thành công tới ThingsBoard")
    else:
        print(f"Kết nối thất bại với mã lỗi {rc}")

def send_data_to_thingsboard(access_token, data):
    client = mqttclient.Client()
    client.username_pw_set(access_token)
    client.on_connect = on_connect
    client.connect(BROKER_ADDRESS, PORT)
    client.loop_start()
    time.sleep(2)
    
    payload = json.dumps(data)
    client.publish("v1/devices/me/attributes", payload, 1)
    print(f"Đã gửi dữ liệu: {payload}")
    
    time.sleep(1)
    client.disconnect()

def control_device(access_token, action, feed_name):
    value = 1 if action == 'on' else 0
    send_data_to_thingsboard(access_token, {feed_name: value})
    print(f"Đã gửi lệnh {value} tới feed '{feed_name}' trên ThingsBoard.")

def control_volume(payload):
    try:
        volume = int(payload)
        os.system(f"amixer sset 'Master' {volume}%")
        print(f"Volume set to {volume}%")
    except ValueError:
        print("Invalid volume value received")

def set_volume(access_token, volume_level):
    feed_name = "speaker.volume"
    send_data_to_thingsboard(access_token, {feed_name: volume_level})
    print(f"Đã gửi mức âm lượng {volume_level} tới feed '{feed_name}' trên ThingsBoard.")

if __name__ == "__main__":
    DEVICE_ACCESS_TOKEN = "ozu62mz72ssdznrcqvhy"  
    control_device(DEVICE_ACCESS_TOKEN, "off", "light.switch")  
    # time.sleep(2)
    # control_device(DEVICE_ACCESS_TOKEN, "off", "light.switch")  
    # set_volume(DEVICE_ACCESS_TOKEN, 50)  # Đặt âm lượng về 50%
