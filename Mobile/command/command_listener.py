import speech_recognition as sr
from audio_utils import speak
import os
from google.cloud import speech
from microphone_stream import MicrophoneStream 
from lms_filter import *
import time
from playsound import playsound
WELCOME_SOUND="command/sound/welcome1.mp3"
ERROR_SOUND="command/sound/end_error.mp3"
MYKEY_PATH = os.path.join(os.getcwd(), "my_key.json")
def listen_commands(max_attempts=1):
    recognizer = sr.Recognizer()
    attempts = 0
    while attempts < max_attempts:
        with sr.Microphone() as source:
            print("Listening........................")
            playsound(WELCOME_SOUND)
            recognizer.adjust_for_ambient_noise(source, duration=1)  
            try:
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)
                command = recognizer.recognize_google(audio, language="vi-VN")
                print(f"Lệnh của bạn: {command}")
                return command.lower()
            except sr.UnknownValueError:
                attempts += 1
                print("Không thể nhận diện được giọng nói.")
                speak("Bạn nói gì tôi nghe không rõ.")
                
            except sr.WaitTimeoutError:
                attempts += 1
                print("Không nghe thấy giọng nói. Hãy thử lại.")
                speak("Môi trường có vẻ hơi ồn, hãy thử lại ở nơi yên tĩnh hơn.")
               
            except sr.RequestError as e:
                print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
                speak("Có vấn đề với kết nối mạng, vui lòng kiểm tra kết nối mạng.")
                
                return None
    speak("Hẹn gặp lại")
    return None


def listen_commands(max_attempts=2, filter_len=5, mu=0.01):
    recognizer = sr.Recognizer()
    attempts = 0
    while attempts < max_attempts:
        with sr.Microphone() as source:
            print("Listening........................")
            
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
                audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
                
                reference_signal = np.random.normal(0, 1, len(audio_data)) 
                
                filtered_audio, weights = lms_filter(audio_data, reference_signal, filter_len, mu)
                
                filtered_audio_bytes = filtered_audio.astype(np.int16).tobytes()
                audio_filtered = sr.AudioData(filtered_audio_bytes, audio.sample_rate, audio.sample_width)

                command = recognizer.recognize_google(audio_filtered, language="vi-VN")
                print(f"Lệnh của bạn: {command}")
                return command.lower()
            except sr.UnknownValueError:
                attempts += 1
                print("Không thể nhận diện được giọng nói.")
                speak("Bạn nói gì tôi nghe không rõ.")
            except sr.WaitTimeoutError:
                attempts += 1
                print("Không nghe thấy giọng nói. Hãy thử lại.")
                speak("Môi trường có vẻ hơi ồn, hãy thử lại ở nơi yên tĩnh hơn.")
            except sr.RequestError as e:
                print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
                speak("Có vấn đề với kết nối mạng, vui lòng kiểm tra kết nối mạng.")
                return None
    speak("Hẹn gặp lại")
    return None

def load_google_credentials():
    credentials_path = MYKEY_PATH
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Không tìm thấy file credentials tại: {credentials_path}")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
load_google_credentials() 
def listen_command(max_attempts=1, timeout_duration=10):
    
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="vi-VN"
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=False  
    )

    attempts = 0
    while attempts < max_attempts:
        try:
            print("Listening........................")
            playsound(WELCOME_SOUND)
            audio_stream = MicrophoneStream(16000, 1024, timeout_duration)  
            with audio_stream as stream:
                audio_generator = stream.generator()
                requests = (speech.StreamingRecognizeRequest(audio_content=content)
                            for content in audio_generator)
                responses = client.streaming_recognize(streaming_config, requests)

                for response in responses:
                    if response.results and response.results[0].is_final:
                        command = response.results[0].alternatives[0].transcript
                        print(f"Lệnh của bạn: {command}")
                        return command.lower()

                if time.time() - audio_stream.start_time > timeout_duration:
                    speak("Bạn nói gì tôi nghe không rõ.")
                    attempts += 1
                    continue  

        except Exception as e:
            attempts += 1
            print(f"Lỗi: {e}")
            speak("Tôi không nghe rõ, vui lòng thử lại.")

    speak("Hẹn gặp lại")
    return None
def standalone_listen():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening........................")
          
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=60, phrase_time_limit=7)
                command = recognizer.recognize_google(audio, language="vi-VN")
                print(f"Lệnh của bạn: {command}")
                return command.lower()
            except sr.RequestError as e:
                print(f"Không thể yêu cầu dịch vụ Google Speech Recognition; {e}")
                speak("Có vấn đề với kết nối mạng, vui lòng kiểm tra kết nối mạng.")
                return None
            except sr.UnknownValueError:
                print("Không thể nhận diện giọng nói. Vui lòng thử lại.")
                continue
