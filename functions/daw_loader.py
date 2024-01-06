import psutil
import time
from threading import Thread
from functions.speak import speak

def daw_loader(main):
	"""	Activates running daws.	"""

	daws_order = ['reaper','live']
	
	def waiting_loop():
		while True:
			
			time.sleep(3)

			for p in psutil.process_iter():

				# Detects Reaper
				if 'reaper' not in main.daws and p.name() == 'reaper.exe':
					reaper_launch()

				# Detects Live
				if 'live' not in main.daws and p.name() == 'Ableton Live 12 Beta.exe':
					live_launch()

			time.sleep(3)

	Thread(target=waiting_loop).start()
	
	def reaper_launch():
		from daw.reaper.reaper import Reaper
		Reaper = Reaper(main)
		main.daws['reaper'] = Reaper
		main.daws_index.append('reaper')
		Reaper.startup()
		speak(Reaper.name+" is active.",printout=True)

	def live_launch():
		from daw.live.live import Live
		Live = Live(main)
		main.daws['live'] = Live
		main.daws_index.append('live')
		Live.startup()
		speak(Live.name+" is active.",printout=True)