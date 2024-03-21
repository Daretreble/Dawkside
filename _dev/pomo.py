import winsound
import random
import os
import time
import accessible_output2.outputs.auto
accessOut = accessible_output2.outputs.auto.Auto()

work_time = 2700 # seconds
messages = ["Enough is enough!","Stop working now!","Stop it..."]
start_time = time.time()
os.system('cls')
load_message = f"Pomodoro started for {round(work_time/60)} minutes"
accessOut.speak(load_message)
print(load_message)
count = 0
Waiting = True
while Waiting:
	time.sleep(60)
	os.system('cls')
	print(f"{count} minute since started")
	count+=1
	Waiting = True if (time.time() - start_time) < work_time else False
print("Stopped!")
while True:
	winsound.Beep(500,200)
	#accessOut.speak(messages[random.randrange(len(messages))])
	time.sleep(5)
