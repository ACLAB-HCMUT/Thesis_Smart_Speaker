# import pveagle
# from pvrecorder import PvRecorder
# from dotenv import load_dotenv
# import os
# load_dotenv()
# script_dir = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_dir)

# access_key = os.getenv("EAGLE_KEY")
# try:
#     eagle_profiler = pveagle.create_profiler(access_key=access_key)
# except pveagle.EagleError as e:
#     print(f"Failed to create Eagle Profiler: {e}")
#     exit(1)


# DEFAULT_DEVICE_INDEX = 1
# recorder = PvRecorder(
#     device_index=DEFAULT_DEVICE_INDEX,
#     frame_length=eagle_profiler.min_enroll_samples
# )

# recorder.start()

# enroll_percentage = 0.0
# while enroll_percentage < 100.0:
  
#     audio_frame = recorder.read()
#     enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
#     print(f"Enrollment: {enroll_percentage:.2f}% - {feedback}")

# recorder.stop()


# speaker_profile = eagle_profiler.export()


# with open("speaker_profile.eagle", "wb") as f:
#     f.write(speaker_profile.to_bytes())

import pveagle
from pvrecorder import PvRecorder
from dotenv import load_dotenv
import os


load_dotenv()
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


access_key = os.getenv("EAGLE_KEY")
if not access_key:
    print("Lỗi: Không tìm thấy EAGLE_KEY trong môi trường.")
    exit(1)


try:
    eagle_profiler = pveagle.create_profiler(access_key=access_key)
except pveagle.EagleError as e:
    print(f"Lỗi khi tạo Eagle Profiler: {e}")
    exit(1)


devices = PvRecorder.get_available_devices()
if not devices:
    print("Không có thiết bị thu âm nào được tìm thấy.")
    exit(1)

print("Danh sách thiết bị thu âm:")
for i, device in enumerate(devices):
    print(f"{i}: {device}")


device_index = 1
if device_index < 0 or device_index >= len(devices):
    print("Chỉ số thiết bị không hợp lệ, sử dụng thiết bị mặc định (1).")
    device_index = 1


recorder = PvRecorder(
    device_index=device_index, 
    frame_length=eagle_profiler.min_enroll_samples
)


enroll_attempts = 3 
recorder.start()
try:
    for attempt in range(enroll_attempts):
        enroll_percentage = 0.0
        print(f"Đang thực hiện lần ghi âm {attempt + 1}...")
        
        while enroll_percentage < 100.0:
            audio_frame = recorder.read()
            enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
            print(f"Enrollment: {enroll_percentage:.2f}% - {feedback}")
finally:
    recorder.stop()
    recorder.delete() 

try:
    speaker_profile = eagle_profiler.export()
    with open("speaker_profile.eagle", "wb") as f:
        f.write(speaker_profile.to_bytes())
    print("Hồ sơ giọng nói đã được lưu thành công.")
except Exception as e:
    print(f"Lỗi khi lưu hồ sơ giọng nói: {e}")
