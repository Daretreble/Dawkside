################################
##                            ##
##   Dawkside                 ##
##   by Patrick Tremblay      ##
##                            ##
##   Under some license.      ##
##   « If you're blind then   ##
##   drive safely. »          ##
##                            ##
################################

# Imports
import psutil
import sys
import os
import time
from classes.main import Main
from functions.speak import speak
from functions.daw_loader import daw_loader
from functions.device_loader import device_loader

if __name__ == "__main__":

	os.system('cls')
	speak("Dawkside is loading using the following devices :\n\n", printout=True)

	dawkside_count = 0
	for process in psutil.process_iter(['pid', 'name']):
		if process.info['name'] == 'dawkside.exe':
			dawkside_count += 1

	if dawkside_count > 1:
		speak("An instance of Dawkside is already running. Exiting.")
		time.sleep(2)
		sys.exit(0)

	# Initialize Main class for global settings
	main = Main()

	#os.system('cls')
	main.play_sound('intro')

	# Load DAWs
	daw_loader(main)
		
	# Load devices
	device_loader(main)

	main.locked = [False, '']
	
	# Intro
	output = f"\nWelcome to Dawkside.\nWaiting for daws.\n"

	speak(output, printout=True)