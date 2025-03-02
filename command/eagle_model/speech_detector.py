import pveagle
from pvrecorder import PvRecorder
import os
from dotenv import load_dotenv
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
load_dotenv()

access_key = os.getenv("EAGLE_KEY")

with open("speaker_profile.eagle", "rb") as f:
    speaker_profile_bytes = f.read()


speaker_profile = pveagle.EagleProfile.from_bytes(speaker_profile_bytes)

try:
   
    eagle = pveagle.create_recognizer(
        access_key=access_key,
        speaker_profiles=[speaker_profile]
    )
except pveagle.EagleError as e:
    print(f"Failed to create Eagle Recognizer: {e}")
    exit(1)


DEFAULT_DEVICE_INDEX = -1  
recorder = PvRecorder(
    device_index=DEFAULT_DEVICE_INDEX,
    frame_length=eagle.frame_length
)

recorder.start()

try:
    while True:
       
        audio_frame = recorder.read()

       
        scores = eagle.process(audio_frame)
        print(scores)
        if scores and scores[0] == 0.0:
            print("Nhận diện thành công!")
        else:
            print("Không phát hiện giọng nói.")

except KeyboardInterrupt:
   
    pass


recorder.stop()
recorder.delete()
eagle.delete()
