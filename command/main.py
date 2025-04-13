# import random
import sys
import os
import time
start_time = time.time()
sys.path.append(os.path.dirname(__file__))
# from notification import monitor_temperature, monitor_moisture
import re
# import threading
import time
start_time = time.time()
from command_processor import process_command,speak
from command_listener import listen_command
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Thời gian thực thi: {execution_time:.4f} giây")
# def import_modules():
#     global process_command, speak, listen_command
#     from command_processor import process_command
#     from audio_utils import speak
#     from command_listener import listen_command
def main():
    
    # import_thread = threading.Thread(target=import_modules)
    # import_thread.start()
    end_keywords_pattern = re.compile(r"\b(hết rồi|hết|kết|kết thúc|cảm ơn|thanks|thank you)\b", re.IGNORECASE)
    # greetings = ["Em nghe", "Dạ", "Có em ạ", "Vâng, em nghe"]
    # follow_up_questions = [
    #     "Em có thể giúp gì nữa ạ?",
    # ]

    # monitor_temperature()
    # monitor_moisture()
    # greeting = random.choice(greetings)
    # import_thread.join()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Thời gian thực thi: {execution_time:.4f} giây")
    # speak(greeting)

    while True:
        
        command = listen_command()
        if command is None:
            print("Terminated due to failure to recognize speech.")
            break
        command= command.lower()
        if end_keywords_pattern.search(command):
            speak("Dạ vâng ạ")
            print(f"End-----------------")
            break
        else:
            end_program=process_command(command)
            # if end_program == 1:
            speak("Hẹn gặp lại")
            print(f"End-----------------")

            break
            # follow_up = random.choice(follow_up_questions)
            # print(follow_up)
            # speak(follow_up)

if __name__ == "__main__":
    main()