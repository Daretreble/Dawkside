import os
import time
from threading import Thread
from functions.speak import speak

def process_loop(self,*args):
	""" Loops through Reapy module for changes. """

	main = self.main
	self.pVar = []
	track = self.track
	id = 0
	self.switchtime = time.time()
	self.loop_switchtime = time.time()
	reset = 0
	
	while True and self.main.running_threads_on:

		if self.datatmp['osc_tracking']['page_change'][0] and time.time() - self.datatmp['osc_tracking']['page_change'][1] > self.switch_delay:
			self.datatmp['osc_tracking']['page_change'][0] = False
			self.devices_manage(action='page_change')
		
		if self.datatmp['osc_tracking']['track_change'][0] and time.time() - self.datatmp['osc_tracking']['track_change'][1] > self.switch_delay:
			main.switchtime = time.time()
			self.plugins.act = False
			to_get = [
				'name',
				'arm',
				'solo',
				'mute',
				'panning',
				'volume',
				'send',
			]
			for _ in to_get:
				if _ == 'send':
					self.fre['track']['send'] = {}
					for send_id in range(6):
						self.client.send_message('/live/track/get/'+_,(self.track.index[0],send_id))	
				else:
					self.client.send_message('/live/track/stop_listen/'+_,(self.track.index[1]))
					self.client.send_message('/live/track/start_listen/'+_,(self.track.index[0]))
			self.client.send_message('/live/song/get/num_tracks',())
			main.switchtime = time.time()
			self.datatmp['osc_tracking']['track_change'][0] = False
			self.pVar = []
			self.switchtime = time.time()
			def track_load():
				time.sleep(0.2)
				track.index[1] = track.index[0]
				self.client.send_message('/live/track/get/devices/name',(track.index[0]))
			Thread(target=track_load).start()
		
		## Timed actions
		if time.time()-self.loop_switchtime > 3:
			self.pVar = ['devices_check']
			self.client.send_message('/live/track/get/devices/name',(track.index[0]))
			self.loop_switchtime = time.time()
		
		time.sleep(0.1)