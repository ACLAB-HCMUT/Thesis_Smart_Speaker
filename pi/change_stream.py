import requests
import json
import sys

# Địa chỉ và cổng của Snapserver
SNAPSERVER_URL = "http://127.0.0.1:1780/jsonrpc"

# Hàm gửi yêu cầu JSON-RPC đến Snapserver
def send_rpc_request(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params if params else {}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(SNAPSERVER_URL, data=json.dumps(payload), headers=headers)
    return response.json()

# Hàm lấy trạng thái hiện tại của Snapserver
def get_server_status():
    return send_rpc_request("Server.GetStatus")

# Hàm tạm dừng nguồn phát nhạc hiện tại
def pause_current_stream(group_id):
    send_rpc_request("Group.SetStream", {"id": group_id, "stream_id": "null"})

# Hàm tiếp tục phát nhạc từ nguồn đã tạm dừng
def resume_stream(group_id, stream_id):
    send_rpc_request("Group.SetStream", {"id": group_id, "stream_id": stream_id})

# Hàm chuyển đổi nguồn nhạc cho tất cả các nhóm
def change_stream_for_all_groups(new_stream_id):
    # Lấy trạng thái hiện tại
    status = get_server_status()

    # Kiểm tra xem có dữ liệu trả về không
    if "result" not in status or "server" not in status["result"]:
        print("Không thể lấy trạng thái từ Snapserver.")
        return

    # Lấy danh sách các nhóm
    groups = status["result"]["server"].get("groups", [])

    # Duyệt qua từng nhóm và chuyển đổi nguồn nhạc
    for group in groups:
        group_id = group.get("id")
        current_stream_id = group.get("stream_id")

        # Nếu nhóm đang sử dụng nguồn nhạc khác, tạm dừng nó và chuyển sang nguồn mới
        if current_stream_id != new_stream_id:
            print(f"Tạm dừng nhóm {group_id} từ {current_stream_id} và chuyển sang {new_stream_id}")
            pause_current_stream(group_id)
            send_rpc_request("Group.SetStream", {"id": group_id, "stream_id": new_stream_id})
        else:
            print(f"Nhóm {group_id} đã sử dụng nguồn nhạc {new_stream_id}, bỏ qua.")

# Hàm chính
if __name__ == "__main__":
    # Kiểm tra xem có tham số dòng lệnh không
    if len(sys.argv) != 2:
        print("Cách sử dụng: python3 change_stream.py <stream_id>")
        print("Ví dụ: python3 change_stream.py Spotify")
        sys.exit(1)

    # Lấy nguồn nhạc mới từ tham số dòng lệnh
    new_stream_id = sys.argv[1]

    # Chuyển đổi nguồn nhạc cho tất cả các nhóm
    change_stream_for_all_groups(new_stream_id)
