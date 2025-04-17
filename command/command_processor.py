import subprocess
import threading
import socket
import json
from chatgpt import get_response
import speech_recognition as sr
from audio_utils import speak
from command_listener import standalone_listen

music_process = None
stop_thread = None

# def send_mpv_command(command):
#     try:
#         client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#         client.connect("/tmp/mpv_socket")
#         client.send((json.dumps(command) + "\n").encode())
#         client.close()
#     except Exception as e:
#         print(" Không gửi được lệnh đến mpv:", e)

# def pause_music():
#     print("⏸ Gửi lệnh pause.")
#     send_mpv_command({ "command": ["set_property", "pause", True] })

# def resume_music():
#     print(" Gửi lệnh resume.")
#     send_mpv_command({ "command": ["set_property", "pause", False] })

# def listen_for_music_commands():
#     while True:
#         command = standalone_listen()
#         if command:
#             command = command.lower()
#             if "Dừng nhạc" in command or "Tắt nhạc" in command or "pause" in command:
#                 speak("Đã dừng nhạc.")
#                 pause_music()
#                 break
#             elif "Tiếp tục" in command or "resume" in command:
#                 speak("Tiếp tục nhạc.")
#                 resume_music()
#                 break

def control_mpv(state):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect("/tmp/mpv_socket")
        client.send((json.dumps(state) + "\n").encode("utf-8"))
        response = client.recv(1024)
        client.close()
        print("🎵 Phản hồi từ mpv:", response.decode("utf-8"))
    except Exception as e:
        print(" Không gửi được lệnh tới mpv:", e)

def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Đang lắng nghe...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio, language='vi-VN').lower()
                print("Nghe được:", command)

                if "stop" in command or "Tắt nhạc" in command or "tắt nhạc" in command:
                    control_mpv("quit")
                    break
                elif "đồng bộ" in command:
                    from send import send_attribute_to_coreiot
                    send_attribute_to_coreiot("fw_tag", "1")
                    continue

                elif "pause" in command or "Tạm dừng" in command or "tạm dừng" in command:
                    control_mpv({ "command": ["set_property", "pause", True] })
                    continue
                elif "resume" in command or "Tiếp tục" in command or "tiếp tục" in command:
                    control_mpv({ "command": ["set_property", "pause", False] })
                    continue
                elif "volume up to 10" in command or "Tăng âm lượng lên 10" in command or "tăng âm lượng lên 10" in command or "tăng âm lượng lên mười" in command or "Tăng âm lượng lên mười" in command:
                    control_mpv({"command": ["add", "volume", 10]})
                    continue
                elif "volume up to 5" in command or "Tăng âm lượng lên 5" in command or "tăng âm lượng lên 5" in command or "tăng âm lượng lên năm" in command or "Tăng âm lượng lên năm" in command:
                    control_mpv({"command": ["add", "volume", 5]})
                    continue
                elif "volume up to 25" in command or "Tăng âm lượng lên 25" in command or "tăng âm lượng lên 25" in command or "tăng âm lượng lên hai mươi lăm" in command or "Tăng âm lượng lên hai lăm" in command:
                    control_mpv({"command": ["add", "volume", 25]})
                    continue
                elif "volume down to 10" in command or "Giảm âm lượng xuống 10" in command or "giảm âm lượng xuống 10" in command or "giảm âm lượng xuống mười" in command or "Giảm âm lượng xuống mười" in command:
                    control_mpv({"command": ["add", "volume", -10]})
                    continue
                elif "volume down to 5" in command or "Giảm âm lượng xuống 5" in command or "giảm âm lượng xuống 5" in command or "giảm âm lượng xuống năm" in command or "Giảm âm lượng xuống năm" in command:
                    control_mpv({"command": ["add", "volume", -5]})
                    continue
                elif "volume down to 25" in command or "Giảm âm lượng xuống 25" in command or "giảm âm lượng xuống 25" in command or "giảm âm lượng xuống hai mươi lăm" in command or "Giảm âm lượng xuống hai lăm" in command:
                    control_mpv({"command": ["add", "volume", -25]})
                    continue

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(" Lỗi kết nối API:", e)
                break

def process_command(command):
    global music_process
    global stop_thread

    command = command.lower()

    if any(keyword in command for keyword in ["phát nhạc", "nhạc", "mở bài"]):
        query = command
        for keyword in ["phát nhạc", "mở nhạc", "mở bài", "đi"]:
            query = query.replace(keyword, "").strip()

        if query:
            speak(f"Đang phát bài {query}")
            print(f"🎵 Đang phát bài: {query}")

            try:
                music_process = subprocess.Popen(["./play_yt.sh", query])
                listener_thread = threading.Thread(target=listen_for_command)
                listener_thread.start()
                # stop_thread = threading.Thread(target=listen_for_music_commands)
                # stop_thread.daemon = True
                # stop_thread.start()
                # music_process.wait()
                # print(" Bài hát đã phát xong.")
                # music_process = None
            except Exception as e:
                print(" Lỗi khi phát nhạc:", e)
                control_mpv("quit")
                return
        else:
            speak("Vui lòng nói rõ tên bài hát bạn muốn phát.")

    # elif "dừng nhạc" in command or "pause" in command:
    #     speak("Đang dừng nhạc.")
    #     pause_music()

    # elif "tiếp tục" in command and "nhạc" in command:
    #     speak("Tiếp tục nhạc.")
    #     resume_music()
    elif "ngưng" and "đồng bộ" in command:
        subprocess.run(["./switch_snapclient.sh", "127.0.0.1"], check=True)
        speak("Đã ngưng đồng bộ.")
    elif "chuyển sang" in command and "youtube" in command:
        subprocess.run(["python", "./change_stream.py", "YouTube"])
        speak("Chuyển sang nguồn nhạc YouTube.")

    elif "chuyển sang" in command and "spotify" in command:
        subprocess.run(["python", "./change_stream.py", "Spotify"])
        speak("Chuyển sang nguồn nhạc Spotify.")
    # if any(keyword in command for keyword in ["8d","8D","tám đê", "8 đê"]):

    #     query = command
    #     for keyword in ["phát nhạc", "mở nhạc", "mở bài","8D", "8d"]:
    #         query = query.replace(keyword, "").strip()
    #     if query:
    #         video_url = search_youtube8(query)
    #         if video_url:
    #             speak(f"Mời bạn nghe nhạc {query}.")
    #             download_and_play_youtube_audio8(video_url)
    #         else:
    #             speak("Không tìm thấy bài hát trên YouTube.")
    #     else:
    #         speak("Vui lòng nói rõ tên bài hát bạn muốn phát.")
    # if any(keyword in command for keyword in ["phát nhạc", "nhạc", "mở bài"]):

    #     query = command
    #     for keyword in ["phát nhạc", "mở nhạc", "mở bài"]:
    #         query = query.replace(keyword, "").strip()
    #     if query:
    #         from music import search_youtube
    #         video_url = search_youtube(query)
    #         if video_url:
    #             from music import download_and_play_youtube_audio
    #             speak(f"Mời bạn nghe nhạc {query}.")
    #             download_and_play_youtube_audio(video_url)
    #         else:
    #             speak("Không tìm thấy bài hát trên YouTube.")
    #     else:
    #         speak("Vui lòng nói rõ tên bài hát bạn muốn phát.")
    elif any(
        keyword in command
        for keyword in ["báo thức", "nhắc nhở", "hẹn giờ"]
    ):
        from reminders import alarm_reminder_action
        print ("process:", command)
        response = alarm_reminder_action(command)
        print(response)
        speak(response)
        return 1
    # elif is_device_command(command):
    #     actions = {
    #         'bật': 'on',
    #         'mở': 'on',
    #         'tắt': 'off',
    #         'đóng': 'off'
    #     }
    #     devices = {
    #         'đèn': 'led1',
    #         'quạt': 'fan',  
    #         'cửa': 'door',
    #         'máy lạnh': 'ac'
    #     }
    #     rooms = ['phòng khách', 'phòng ngủ', 'phòng bếp']

    #     room_pattern = r'\b(' + '|'.join(rooms) + r')\b'
    #     device_pattern = r'\b(' + '|'.join(devices) + r')\b'
    #     action_pattern = r'\b(' + '|'.join(actions.keys()) + r')\b'

    #     room_match = re.search(room_pattern, command, re.IGNORECASE)
    #     device_match = re.search(device_pattern, command, re.IGNORECASE)
    #     action_match = re.search(action_pattern, command, re.IGNORECASE)
    #     response=""
        
    #     # case 1: full command
    #     if room_match and device_match and action_match:
    #         check=control(command)
    #         # if check==1:
    #         #     return 1 
    #         response="Em đã thực hiện lệnh ạ."           
    #     # case 2: missing device, but room, action are present
    #     elif room_match and action_match and not device_match:
    #         room = room_match.group(0)
    #         action = actions[action_match.group(0).lower()]
    #         response=f"Vui lòng chỉ định thiết bị để {action_match.group(0).lower()} ở {room}."

    #     # case 3: missing action, but room, device are present
    #     elif room_match and device_match and not action_match:
    #         room = room_match.group(0)
    #         device = device_match.group(0)
    #         response=f"Vui lòng chỉ định hành động cho {device} ở {room}."
        
    #     # case 4: room mentioned but missing both action and device
    #     elif room_match and not action_match and not device_match:
    #         room = room_match.group(0)
    #         response=f"Vui lòng chỉ định thiết bị và hành động ở {room}."
    #     elif action_match and device_match and not room_match:
    #         device = device_match.group(0)
    #         action = action_match.group(0)
    #         response = f"Vui lòng chỉ định phòng để {action_match.group(0).lower()} {device}."
    #     elif action_match and device_match and not room_match:
    #         device = device_match.group(0)
    #         action = action_match.group(0)
    #         response = f"Vui lòng chỉ định phòng để {action_match.group(0).lower()} {device}."
    #     # case 5: command not recognized
    #     else:
    #         response="Lệnh không được nhận diện, vui lòng thử lại."
        
    #     print(response)
    #     speak(response)
    elif command =="hôm nay":
        from weather import fetch_weather_data
        from time_utils import get_current_date_vn_format
        today= get_current_date_vn_format()
        today += " "
        today += fetch_weather_data()
        speak(today)
    elif command=="thời tiết" or command=="thời tiết hôm nay":
        from weather import fetch_weather_data 
        speak(fetch_weather_data())

    elif any(
        keyword in command
        for keyword in ["giọng nữ", "giọng con gái", "giọng đàn bà", "giọng phụ nữ"]
    ):
        from audio_utils import set_default_voice
        set_default_voice("female")
        return 
    elif any(
        keyword in command
        for keyword in ["giọng nam", "giọng con trai", "giọng đàn ông"]
    ):
        from audio_utils import set_default_voice
        set_default_voice("male")
        return
    # elif "giọng mặc định" in command:
    #     set_default_voice("default")
    #     return
    elif any(
        keyword in command
        for keyword in ["lấy lịch", "xem lịch", "hiển thị lịch", "danh sách sự kiện", "xem sự kiện"]
    ):  
        from my_calendar import get_calendar_events
        print("Đang lấy danh sách sự kiện...")
        speak(get_calendar_events())
    elif any(
         keyword in command
         for keyword in ["tìm điện thoại", "tìm", "kiếm điện thoại","kiếm"]
     ):  
         
         make_call()
         speak("Đang nhá máy điện thoại")
    elif any(
        keyword in command
        for keyword in [
            "bây giờ là mấy giờ",
            "mấy giờ rồi",
            "giờ hiện tại",
            "bây giờ đang là mấy giờ",
            "hiện tại đang mấy giờ",
            "hiện tại mấy giờ",
        ]
    ):  
        from time_utils import get_current_time
        get_current_time()
    elif any(
        keyword in command
        for keyword in ["xóa sự kiện", "gỡ sự kiện", "xóa lịch", "gỡ lịch", "hủy sự kiện"]
    ):
        print("Đang xóa sự kiện...")

        if "vào" in command or "ngày" in command:
            from my_calendar import extract_time_from_command
            time_to_delete = extract_time_from_command(command)
            if time_to_delete:
                from my_calendar import delete_event_by_name_or_time
                response = delete_event_by_name_or_time(start_time=time_to_delete)
                print(f"Đã xóa sự kiện vào {time_to_delete}.")
            else:
                response = "Không thể xác định thời gian của sự kiện. Vui lòng thử lại."
            speak(response)

        else:
            from my_calendar import extract_event_name_from_command
            event_name = extract_event_name_from_command(command)
            if event_name:
                from my_calendar import delete_event_by_name_or_time
                response = delete_event_by_name_or_time(summary=event_name)
                print(f"Đã xóa sự kiện '{event_name}'.")
            else:
                response = "Vui lòng cung cấp tên sự kiện bạn muốn xóa."
                speak(response)

        print(response)
        speak(response)
    elif any(
        keyword in command for keyword in ["thêm sự kiện", "tạo sự kiện", "lên sự kiện","thêm lịch", "lên lịch"]
    ):  
        from my_calendar import input_for_add_event
        input_for_add_event()  # add_event inside here
        # print("Đang tạo sự kiện mới...")
        # summary = "Họp nhóm dự án"
        # location = "Hồ Chí Minh, Việt Nam"
        # description = "Thảo luận tiến độ dự án."
        # start_time = "2024-11-24T10:00:00+07:00"
        # end_time = "2024-11-24T11:00:00+07:00"
        # add_event(summary, location, description, start_time, end_time)
    # elif "bật cảm biến" in command or "tắt cảm biến" in command:
    #     if "độ ẩm" in command:
    #         if "bật" in command:
    #             set_sensor_status(MOISTURE_FEED, True)
    #         elif "tắt" in command:
    #             set_sensor_status(MOISTURE_FEED, False)
    #     elif "nhiệt độ" in command:
    #         if "bật" in command:
    #             set_sensor_status(TEMPERATURE_FEED, True)
    #         elif "tắt" in command:
    #             set_sensor_status(TEMPERATURE_FEED, False)
    # elif "âm lượng" in command or "loa" in command:
    #     volume_level = re.search(r"\d+", command)
    #     if volume_level:
    #         volume_level = int(volume_level.group())
    #         if volume_level > 100:
    #             volume_level = 100
    #         elif volume_level < 0:
    #             volume_level = 0
    #     else:
    #         volume_level = 50
    #     set_volume(volume_level)
    #     response = f"Đã điều chỉnh âm lượng đến {volume_level}%."
    #     print(response)
    #     speak(response)
    elif any(keyword in command for keyword in ["dừng nhạc", "tắt nhạc"]):
        from music import stop_music
        stop_music()
        # stop_music8()

    elif "kêu" in command or ("tiếng" in command and "kêu" in command):
        from kid_mode import play_sound_animal
        play_sound_animal(command)
    elif "kể" in command and ("truyện" in command or "chuyện" in command):
        print("Đang kể truyện...")
        from kid_mode import play_story_sound
        play_story_sound()
    elif any(keyword in command for keyword in ["đường từ", "tìm đường", "chỉ đường", "hướng dẫn đường", "đường đi từ", "hỏi đường"]):
        from navigation import process_direction
        process_direction(command)
    elif any(
        keyword in command
        for keyword in ["thời tiết", "tin tức", "hôm nay", "hiện nay", "thời sự"]
    ):  
        from search_agent import search_and_summarize
        tavily_answer = search_and_summarize(command)
        speak(tavily_answer)
        print(f"Final Answer: {tavily_answer}")
                
    # elif any(
    #     keyword in command
    #     for keyword in [
    #         "căn",
    #         "giai thừa",
    #         "đạo hàm",
    #         "tích phân",
    #         "bình phương",
    #         "phép tính",
    #         "chia",
    #         "nhân",
    #         "cộng",
    #         "trừ",
    #         "hàm số mũ",
    #         "logarit",
    #         "lập phương",
    #         "+",
    #         "/",
    #         "x",
    #     ]
    # ):
    #     try:
    #         result = math_calculation(command)
    #         print(f"Kết quả toán học: {result}")
    #         speak(result)
    #     except Exception as e:
    #         print(f"Lỗi xử lý toán học: {e}")
    #         speak("Xin lỗi, tôi không thể xử lý phép toán này.")
    else:
        print("Gửi yêu cầu đến ChatGPT API...")
        
        chatgpt_answer = get_response(command)
        print(f"ChatGPT trả lời: {chatgpt_answer}")
        speak(chatgpt_answer)

# make_call()