from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
from google.cloud import texttospeech
import os
# SOUND_PATH = "command/sound/command.mp3" 
# MYKEY_PATH = "command/my_key.json"
SOUND_PATH = "sound/command.mp3" 
MYKEY_PATH = "my_key.json"
default_voice="default"
def load_google_credentials():
   
    credentials_path = MYKEY_PATH
    
   
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Không tìm thấy file credentials tại: {credentials_path}")
    
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    print(f"Đã load credentials từ: {credentials_path}")
load_google_credentials()
def speak_female(text):
    try:
        client = texttospeech.TextToSpeechClient()

        input_text = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="vi-VN",  
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3  
        )

        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
       
        output_file = SOUND_PATH
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        playsound(output_file)

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def speak_male(text):
    try:
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="vi-VN",  
            name="vi-VN-Standard-B",  
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3  
        )
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        output_file = SOUND_PATH
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        playsound(output_file)

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
def set_default_voice(voice):
    global default_voice
    actions = {
        "male": ("Đã chuyển sang giọng nam.", "Đã chuyển sang giọng nam."),
        "female": ("Đã chuyển sang giọng nữ.", "Đã chuyển sang giọng nữ."),
        "default": ("Đã chuyển sang giọng mặc định.", "Đã chuyển sang giọng mặc định."),
    }
    if voice in actions:
        default_voice = voice
        message, speak_text = actions[voice]  
        print(message)
        speak(speak_text) 
    else:
        print("Giọng không hợp lệ. Vui lòng chọn 'male', 'female', hoặc 'default'.")
def speak(text):
    global default_voice 
    
    try:
        if default_voice == "male":
            speak_male(text)
        elif default_voice == "female":
            speak_female(text)
        else:
            speak_female(text)
            # tts = gTTS(text=text, lang='vi')
            # tts.save(SOUND_PATH)
            # audio = AudioSegment.from_file(SOUND_PATH)
            # audio = audio.speedup(playback_speed=1.25)
            # audio.export(SOUND_PATH, format="mp3")
            # playsound(SOUND_PATH)
    except Exception as e:
        print(f"Lỗi: {e}")

# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Neural2-D
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-A
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-B
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-C
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Standard-D
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-A
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-B
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-C
# Ngôn ngữ: ['vi-VN']
# SSML Gender: FEMALE
# Tần số mẫu: 24000
# ------------------------------
# Tên giọng: vi-VN-Wavenet-D
# Ngôn ngữ: ['vi-VN']
# SSML Gender: MALE
# Tần số mẫu: 24000
