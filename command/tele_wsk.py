import socket
import threading
import pickle
import pyaudio

# partner_ip = "192.168.137.128"  # IP Address của máy kia
port_send = 8080
port_receive = 9090 

FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 44100  
CHUNK = 1024

audio = pyaudio.PyAudio()

stream_in = audio.open(format=FORMAT, channels=CHANNELS,
                       rate=RATE, input=True, frames_per_buffer=CHUNK)

stream_out = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True, frames_per_buffer=CHUNK)

def send_audio(partner_ip):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print(f"🔊 Gửi âm thanh đến {partner_ip}:{port_send}...")

    while True:
        try:
            frame = stream_in.read(CHUNK, exception_on_overflow=False) 
            data = pickle.dumps(frame) 
            udp_socket.sendto(data, (partner_ip, port_send))
        except Exception as e:
            print(f"❌ Lỗi gửi âm thanh: {e}")
            break

def receive_audio():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", port_receive))
    print(f"🎧 Nhận âm thanh trên cổng {port_receive}...")

    while True:
        try:
            data, addr = udp_socket.recvfrom(65536)  
            frame = pickle.loads(data)  
            stream_out.write(frame)
        except Exception as e:
            print(f"❌ Lỗi nhận âm thanh: {e}")
            break

def tele_wsk(partner_ip):
    receive_thread = threading.Thread(target=receive_audio, daemon=True)
    send_thread = threading.Thread(target=send_audio, args=(partner_ip, ), daemon=True)

    receive_thread.start()
    send_thread.start()

    while True:
        pass
