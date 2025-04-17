# import time
# import json
# import paho.mqtt.client as mqtt

# THINGSBOARD_HOST = "app.coreiot.io"
# ACCESS_TOKEN = "ozu62mz72ssdznrcqvhy"  

# attribute_data = {
#     "fw_tag": "0",

# }

# def on_connect(client, userdata, flags, rc):
#     print("�� k?t n?i t?i CoreIoT (rc={})".format(rc))
#     client.publish("v1/devices/me/attributes", json.dumps(attribute_data), qos=1)
#     print("�� g?i d? li?u attributes l�n ThingsBoard/CoreIoT.")

# client = mqtt.Client()
# client.username_pw_set(ACCESS_TOKEN)
# client.on_connect = on_connect

# client.connect(THINGSBOARD_HOST, 1883, 60)
# client.loop_start()

# time.sleep(3)
# client.loop_stop()
# client.disconnect()
# print("ng?t k?t n?i.")
#!/usr/bin/env python3
import time
import json
import paho.mqtt.client as mqtt

THINGSBOARD_HOST = "app.coreiot.io"
ACCESS_TOKEN = "ozu62mz72ssdznrcqvhy"

def send_attribute_to_coreiot(key, value):
    attribute_data = {
        key: value
    }

    def on_connect(client, userdata, flags, rc):
        print(" ket noi toi CoreIoT (rc={})".format(rc))
        client.publish("v1/devices/me/attributes", json.dumps(attribute_data), qos=1)
        print(f" da gui: {attribute_data}")

    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.on_connect = on_connect

    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_start()
    time.sleep(3)  
    client.loop_stop()
    client.disconnect()
    print("ngat ket noi.\n")


if __name__ == "__main__":
    send_attribute_to_coreiot("fw_tag", 1)