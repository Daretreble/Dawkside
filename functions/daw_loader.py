import psutil
import time
from functions.speak import speak

def daw_loader(main):
	"""	Activates running daws.	"""

	daws_order = ['reaper','live']
	
	if len(main.daws) == 0:

		print('Scanning for daws.')
	
		for p in psutil.process_iter():
				
			# Load Reaper
			if 'reaper' not in main.daws and p.name() == 'reaper.exe':
				from daw.reaper.reaper import Reaper
				Reaper = Reaper(main)
				main.daws['reaper'] = Reaper
				time.sleep(5)
				Reaper.startup()
				speak("Reaper is running.",printout=True)
			
			# Load Ableton Live
			if 'live' not in main.daws and "Ableton Live" in p.name():
				from daw.live.live import Live
				Live = Live(main)
				main.daws['live'] = Live
				Live.startup()


		for _ in daws_order:
			if _ in main.daws:
				main.daws_index.append(_)