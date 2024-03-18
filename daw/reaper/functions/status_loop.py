import os
import sys
import time
import pprint
import re
from threading import Thread
from functions.speak import speak

def status_loop(self,*args):
	""" Loops through Reapy module for changes. """

	plugins = self.plugins
	
	self.pVar = []
	track = False
	id = 0
	changed = False
	self.switchtime = time.time()
	sendTmp = False
	recvTmp = False
	reset = 0
	
	if self.reapy_mode:
		
		while True:

			if 'stop' in self.pVar:
				break
				speak("Locked on track "+self.name)
			
			if 'trackreload' in self.pVar:
				changed = True
				
			if 'fxreload' in self.pVar and time.time() - self.main.switchtime > self.switch_delay:
				self.get_data(['fx'])
				self.pVar = []
				
			try:
				track = self.reapy.Project().selected_tracks[0]
			except AttributeError:
				time.sleep(5)
				track = self.reapy.Project().selected_tracks[0]
			except ConnectionResetError:
				self.quit()
				break
			except IndexError:
				track = self.reapy.Project().master_track
			if track:
				if changed:
					if time.time() - self.switchtime > self.switch_delay:
						self.lastact = ''
						self.track.reapy_track = track
						self.get_data(['track','sendrecv','fx','plugins'])
						changed = False
						self.pVar = []
						self.switchtime = time.time()
						plugins.index[1] = plugins.index[0]
						plugins.page[2] = plugins.page[0]
				
				if id != track.id:
					id = track.id
					self.switch_on = True
					changed = True
					self.switchtime = time.time()
				
				if plugins.index[1] != plugins.index[0] and time.time()-self.main.switchtime >= self.switch_delay:
					self.get_data(['fx'])
					plugins.index[1] = plugins.index[0]
					self.track.history[track.id]['fx'] = plugins.index[0]
				
				if plugins.page[2] != plugins.page[0] and time.time()-self.main.switchtime >= self.switch_delay:
					self.get_data(['fx'])
					plugins.page[2] = plugins.page[0]
					self.track.history[track.id]['pg'] = plugins.page[0]
			
			if changed:
				reset = 0
			else:
				reset += 1
			if reset > 30:

				# Check new sends
				sendTmp = track.n_sends
				recvTmp = track.n_receives
				if self.track.nsend != sendTmp or self.track.nrecv != recvTmp:
					self.get_data(['sendrecv'])
				self.track.nsend = int(sendTmp)
				self.track.nrecv = (recvTmp)
				
				# Check plugins list changes
				fxTmp = track.n_fxs
				if plugins.nfxs != fxTmp:
					self.get_data(['fx','plugins'])
				reset = 0
				
			time.sleep(0.1)

	else:

		while True and 'quit' not in self.pVar:

			if 'page_change' in self.pVar and time.time()-self.switchtime > 0.5:
				self.pVar = []
				plugins.user.manage()
				plugins.user.refresh(action='full')
				main.play_sound('ready')
				#self.main.play_sound('ready')

			if 'trackreload' in self.pVar and time.time()-self.switchtime > 0.4:
				self.pVar = []
				self.switchtime = time.time()
				def delayed_load():
					time.sleep(0.2)
					count = 0
					self.fre['track']['send'] = {}
					self.fre['track']['recv'] = {}
					for cat in ['send','recv']:
						for key,value in self.plugins.sendrecv_tmp[cat].items():
							pattern = r"(Send|Recv) \d+"
							if not re.match(pattern,value['name']):
								self.fre['track'][cat][key-1] = value
					for key,value in plugins.params.items():
						if value['name'] == '':
							if key in plugins.params:
								pass
								#plugins.params.pop(key)
						else:
							count += 1
					plugins.param_count = count
					plugins.user.manage()
					self.track.refresh(action='full')
					plugins.user.refresh(action='full')
					self.switch_on = False
					main.play_sound('ready')
					#self.main.play_sound('ready')
				Thread(target=delayed_load).start()
				self.client.send_message('/device/fxparam/count',256)

			time.sleep(0.1)