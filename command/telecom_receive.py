import socket
import threading
import pickle
import alsaaudio
import time
import sys

import socket
import os
import pyttsx3
import speech_recognition as sr

CHANNELS = 1
RATE = 44100
CHUNK = 1024

stop_event = threading.Event()

######################## LIST DEVICE IP & PORT
# kitchen_ip: this device (192.168.137.76)
bed_room_ip = "192.168.137.84"
living_room_ip = "192.168.137.175"
port_send = 8080
port_receive = 9090
#########################


# engine = pyttsx3.init()
# recognizer = sr.Recognizer()
# mic = sr.Microphone()


# input_device = alsaaudio.PCM(
#     type=alsaaudio.PCM_CAPTURE,
#     mode=alsaaudio.PCM_NORMAL,
#     channels=CHANNELS,
#     rate=RATE,
#     format=alsaaudio.PCM_FORMAT_S16_LE,
#     periodsize=CHUNK
# )

output_device = alsaaudio.PCM(
    type=alsaaudio.PCM_PLAYBACK,
    mode=alsaaudio.PCM_NORMAL,
    channels=CHANNELS,
    rate=RATE,
    format=alsaaudio.PCM_FORMAT_S16_LE,
    periodsize=CHUNK
)

def receive_audio(udp_socket):
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # udp_socket.bind(("0.0.0.0", port_receive))
    print(f"Nhận âm thanh trên cổng {port_receive}...")

    while True:
        try:
            data, addr = udp_socket.recvfrom(4096)
            output_device.write(data)
        except Exception as e:
            print(f"Lỗi nhận âm thanh: {e}")
            break

def receive_call():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind(("0.0.0.0", port_receive))
    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            if data == b"RQBED":
                print("Nhận cuộc gọi từ phòng ngủ")
                udp_socket.sendto(b"YES", (bed_room_ip, port_send))
                print("Đã gửi phản hồi tới phòng ngủ")
                receive_audio(udp_socket)

            elif data == b"RQLIV":
                print("Nhận cuộc gọi từ phòng khách")
                udp_socket.sendto(b"YES", (living_room_ip, port_send))
                print("Đã gửi phản hồi tới phòng khách")
                receive_audio(udp_socket)
                
            else:
                print("Chưa có cuộc gọi nào")

        except Exception as e:
            print(f"Lỗi: {e}")
            break



def main(args):
    param_str = args[0].strip().lower()
    if param_str != "f":
        detected_flag = True
    else:
        detected_flag = False

    receive_call_thread = threading.Thread(target=receive_call, daemon=True)

    if detected_flag == True:
        stop_event.set()
        receive_call_thread.join()
    else:
        receive_call_thread.start() 
        time.sleep(1)
    # except KeyboardInterrupt:
    #     print("\n Dừng chương trình.")

    # while(1):
        
       
            # engine.say("Cuộc gọi từ phòng ngủ, bạn đồng ý hay từ chối?")
            # engine.runAndWait()

            # with mic as source:
            #     print("Hãy nói 'đồng ý' hoặc 'từ chối'")
            #     recognizer.adjust_for_ambient_noise(source)
            #     audio = recognizer.listen(source)

            # response = recognizer.recognize_google(audio, language="vi-VN")
            # print(f"Bạn nói: {response}")
            
            # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # if "đồng ý" in response.lower():
            #     udp_socket.sendto(b"YES", (bed_room_ip, port_send))
            #     print("Đã gửi phản hồi tới phòng ngủ")
            #     udp_socket.close()
            #     receive_call(port_receive)
            # elif "từ chối" in response.lower():
            #     udp_socket.sendto(b"NO", (bed_room_ip, port_send))
            #     print("Đã gửi phản hồi tới phòng ngủ")
            #     udp_socket.close()
            #     return



        #     engine.say("Cuộc gọi từ phòng ngủ, bạn đồng ý hay từ chối?")
        #     engine.runAndWait()

        #     with mic as source:
        #         print("Hãy nói 'đồng ý' hoặc 'từ chối'")
        #         recognizer.adjust_for_ambient_noise(source)
        #         audio = recognizer.listen(source)

        #     response = recognizer.recognize_google(audio, language="vi-VN")
        #     print(f"Bạn nói: {response}")
            
        #     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
        #     if "đồng ý" in response:
        #         udp_socket.sendto(b"YES", (living_room_ip, port_send))
        #         print("Đã gửi phản hồi tới phòng khách")
        #         udp_socket.close()
        #         receive_call(port_receive)
        #     elif "từ chối" in response:
        #         udp_socket.sendto(b"NO", (living_room_ip, port_send))
        #         print("Đã gửi phản hồi tới phòng khách")
        #         udp_socket.close()
        #         return
        # else:
        #     udp_socket.close()
        #     continue
        
if __name__ == "__main__":
    main(sys.argv[1:])

