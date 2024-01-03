import os
import time
from functions.speak import speak
from threading import Thread

def process_loop(self,*args):
	""" Loops through Reapy module for changes. """

	main = self.main
	self.pVar = []
	track = self.track
	id = 0
	changed = False
	self.switchtime = time.time()
	loop_switchtime = time.time()
	reset = 0
	
	while True and self.main.running_threads_on:

		if self.datatmp['track_change']:
			changed = True
		
		if self.datatmp['track_change']:
			if time.time() - self.switchtime > self.switch_delay:
				main.switchtime = time.time()
				self.plugins.act = False
				to_get = [
					'name',
					'arm',
					'solo',
					'mute',
					'panning',
					'volume',
				]
				for _ in to_get:
					self.client.send_message('/live/track/stop_listen/'+_,(self.track.index[1]))
					self.client.send_message('/live/track/start_listen/'+_,(self.track.index[0]))
				self.client.send_message('/live/song/get/num_tracks',())
				main.switchtime = time.time()
				self.datatmp['track_change'] = False
				self.pVar = []
				self.switchtime = time.time()
				def track_load():
					time.sleep(0.2)
					track.index[1] = track.index[0]
					self.client.send_message('/live/track/get/devices/name',(track.index[0]))
					main.play_sound('ready')
				Thread(target=track_load).start()
		
		# Sample of action each 2 seconds
		"""
		if time.time()-loop_switchtime > 2:
			pass
			loop_switchtime = time.time()
		"""
		
		time.sleep(0.1)