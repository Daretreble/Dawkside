import os
import time
import pprint
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
	
	while True:

		if self.datatmp['osc_tracking']['page_change'][0] and time.time() - self.datatmp['osc_tracking']['page_change'][1] > self.switch_delay:
			self.datatmp['osc_tracking']['page_change'][0] = False
			self.devices_manage(action='page_change')
		
		if self.datatmp['osc_tracking']['scene_change'][0] and time.time() - self.datatmp['osc_tracking']['scene_change'][1] > 0.3:
			self.pVar = []
			self.datatmp['osc_tracking']['scene_change'][0] = False
			"""
			self.clips.row = {}
			for t in range(self.tracks.num[0]):
				self.clips.row.append(None)
				self.client.send_message('/live/clip_/get/has_clip',(t,self.scenes.index[0]))
			def scene_load():
				time.sleep(0.5)
				os.system('cls')
				pprint.pprint(self.clips.row)
			Thread(target=scene_load).start()
			"""
		
		if self.datatmp['osc_tracking']['track_change'][0] and time.time() - self.datatmp['osc_tracking']['track_change'][1] > self.switch_delay:
			self.plugins.act = False
			to_get = [
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
					for send_id in range(2):
						self.client.send_message('/live/track/get/'+_,(self.track.index[0],send_id))	
				else:
					pass
					#self.client.send_message('/live/track/stop_listen/'+_,(self.track.index[1]))
					#self.client.send_message('/live/track/start_listen/'+_,(self.track.index[0]))
			self.datatmp['osc_tracking']['track_change'][0] = False
			self.pVar = []
			def track_load():
				time.sleep(0.1)
				track.index[1] = track.index[0]
				self.client.send_message('/live/track/get/devices/name',(track.index[0]))
			Thread(target=track_load).start()
		
		## Timed actions
		if not self.datatmp['osc_tracking']['page_load'][0] and time.time()-self.loop_switchtime > 2:
			self.client.send_message('/live/song/get/num_tracks',())
			self.client.send_message('/live/song/get/num_scenes',())
			self.pVar = ['devices_check']
			self.client.send_message('/live/track/get/devices/name',(track.index[0]))
			self.loop_switchtime = time.time()
		
		time.sleep(0.1)