import socket
import threading
import pickle
import alsaaudio
import time

CHANNELS = 1
RATE = 44100
CHUNK = 1024

######################## LIST DEVICE IP & PORT
# kitchen_ip: this device (192.168.137.76)
bed_room_ip = "192.168.137.84"
living_room_ip = "192.168.137.175"
port_send = 8080
port_receive = 9090
#########################

input_device = alsaaudio.PCM(
    type=alsaaudio.PCM_CAPTURE,
    mode=alsaaudio.PCM_NORMAL,
    channels=CHANNELS,
    rate=RATE,
    format=alsaaudio.PCM_FORMAT_S16_LE,
    periodsize=CHUNK
)

output_device = alsaaudio.PCM(
    type=alsaaudio.PCM_PLAYBACK,
    mode=alsaaudio.PCM_NORMAL,
    channels=CHANNELS,
    rate=RATE,
    format=alsaaudio.PCM_FORMAT_S16_LE,
    periodsize=CHUNK
)

def send_audio(partner_ip, port_send, udp_socket):
    print(f"Gửi âm thanh đến {partner_ip}:{port_send}...")

    while True:
        try:
            length, frame = input_device.read()
            if length > 0:
                udp_socket.sendto(frame, (partner_ip, port_send))
        except Exception as e:
            print(f"Lỗi gửi âm thanh: {e}")
            break

def send_call(partner_ip, port_send, udp_socket):
    send_thread = threading.Thread(target=send_audio, args=(partner_ip, port_send, udp_socket), daemon=True)
    send_thread.start()
    try: 
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Dừng chương trình.")

def request_call(command):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", port_receive))

    if "ngủ" in command.lower():
        udp_socket.sendto(b"RQKIT", (bed_room_ip, port_send))
        print("Đã gửi yêu cầu gọi tới phòng ngủ")
        while True:
            try:
                data, addr = udp_socket.recvfrom(4096)
                if data == b"YES":
                    send_call(bed_room_ip, port_send, udp_socket)
            except Exception as e:
                print(f"Lỗi: {e}")
                break

    elif "khách" in command.lower():
        udp_socket.sendto(b"RQKIT", (living_room_ip, port_send))
        print("Đã gửi yêu cầu gọi tới phòng khách")
        while True:
            try:
                # data, addr = udp_socket.recvfrom(4096)
                # if data == b"YES":
                    send_call(living_room_ip, port_send, udp_socket)
            except Exception as e:
                print(f"Lỗi: {e}")
                break
