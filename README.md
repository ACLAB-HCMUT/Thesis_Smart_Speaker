# Thesis_Smart_Speaker-
	Thesis research and implementation Smart Speaker for smart home applications

# Folder speed_reg-vx: Recognition Speed from User
	Input: voice of User from Microphone of Jabra Speaker
	Output: % of each Label (RECOMMEND: 2 Label, Build more 2 can make file bin run very LONGG)
	Improve Point: Increase performance of Model (Distinguish noise, talking sound with "phip") and can Detect "phip" in normal distance
	speed_reg-v14: initial version
	speed_reg-v19: so much Label, file Bin can't run fast (CANCELLED) 
	speed_reg-v21: Recognize User voice (in short distance)
	speed_reg-v23: Recognize User Voice (in short distance and long distance)
 	phip-v1: Recoginize Wake-up Word with new word:"phip", more effect, threshold on Pi: 0.49
  	phip-v2: High Accuracy and Performance. But quite hard to detect wake word:"phip" from microphone of Jabra speaker, threshold on Pi: 0.5
   	phip-v3: (currently): easier detect label:"phip" than phip-v2. Still wrong triggle with some word have the same pronounciation, theshold on Pi: 0.5
-------------------------------------------------------------------------------------
# File __init__.py: 
	Used for main.cpp know directory of command/process, etc
-------------------------------------------------------------------------------------
# Mosquitto on Raspberry Pi 4

 	The overview of the broker
![image](https://github.com/user-attachments/assets/db553824-80a2-4449-af2b-5ba65b56be1f)

	**MQTT Mosquitto Broker**
![image](https://github.com/user-attachments/assets/79e91a12-e6e3-4e8c-9938-a68d36d049c0)

