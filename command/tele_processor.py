import socket

bed_room_ip = "192.168.137.128"
living_room_ip = "192.168.137.175"
port_send = 8080
port_receive = 9090 

def request_call(command):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if "phòng ngủ" in command.lower():
        udp_socket.sendto(b"CALL_REQUEST", (bed_room_ip, port_send))
        print("📞 Đã gửi yêu cầu gọi tới phòng ngủ")
        udp_socket.bind(("0.0.0.0", port_receive))
        data, addr = udp_socket.recvfrom(1024)
        if data != b"YES":
            return ""
        else:
            return bed_room_ip
    elif "phòng khách" in command.lower():
        udp_socket.sendto(b"CALL_REQUEST", (living_room_ip, port_send))
        print("📞 Đã gửi yêu cầu gọi tới phòng khách")
        udp_socket.bind(("0.0.0.0", port_receive))
        data, addr = udp_socket.recvfrom(1024)
        if data != b"YES":
            return ""
        else:
            return living_room_ip
    else:
        return ""