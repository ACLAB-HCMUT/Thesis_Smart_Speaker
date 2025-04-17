#!/usr/bin/env python3
import time
import json
import sys
import paho.mqtt.client as mqtt
import subprocess
from send import send_attribute_to_coreiot
THINGSBOARD_HOST = "app.coreiot.io"
ACCESS_TOKEN = "ozu62mz72ssdznrcqvhy" 

ATTRIBUTE_REQUEST_ID = 1
SHARED_ATTRIBUTES = ["fw_tag"]

def on_connect(client, userdata, flags, rc):
    # print("Da ket noi voi CoreIoT (rc={})".format(rc))
    print("da ket noi iot")
    
    request_payload = {
        "clientKeys": ",".join(SHARED_ATTRIBUTES),
        "sharedKeys": ",".join(SHARED_ATTRIBUTES)
    }
    
    client.publish(f"v1/devices/me/attributes/request/{ATTRIBUTE_REQUEST_ID}",
                   json.dumps(request_payload),
                   qos=1)

def on_message(client, userdata, msg):
    # print("Da nhan du lieu:")
    # print(f"TOPIC: {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        fw_tag = payload.get("client", {}).get("fw_tag")
        # print("===============")
        # print(type(fw_tag))
        # print("===============")
        if fw_tag is not None:
            if fw_tag == 1:
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print("1")

                # try:
                #     subprocess.Popen(["./switch_snapclient.sh"], check=True)
                # except subprocess.CalledProcessError as e:
                #     print(f"L?i khi ch?y script: {e}")
                # send_attribute_to_coreiot("fw_tag", "0")
                client.loop_stop()
                client.disconnect()
                
                sys.exit(0) 
            elif fw_tag ==2:
                print("2")
                client.loop_stop()
                client.disconnect()
                # send_attribute_to_coreiot("fw_tag", "0")
                sys.exit(0) 
            # else:
            #     print("type")
            #     print(type(fw_tag))
            #     print(f"fw_tag nhan duoc: {fw_tag}")
            #     client.loop_stop()
            #     client.disconnect()
            #     sys.exit(0)
        else:
            print("Khong tim thay fw_tag trong du lieu.")
            client.loop_stop()
            client.disconnect()
            sys.exit(1)

    except Exception as e:
        print("Loi khi doc payload:", e)
        client.loop_stop()
        client.disconnect()
        sys.exit(1)

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.on_connect = on_connect
client.on_message = on_message

client.connect(THINGSBOARD_HOST, 1883, 60)
client.subscribe("v1/devices/me/attributes/response/+")
client.loop_start()

time.sleep(10)
client.loop_stop()
client.disconnect()
sys.exit(1)