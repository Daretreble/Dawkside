import os
import time
from functions.speak import speak

def reapy_loop(self,*args):
	""" Loops through Reapy module for changes. """

	self.pVar = []
	track = False
	id = 0
	changed = False
	self.switchtime = time.time()
	sendTmp = False
	recvTmp = False
	reset = 0
	
	while True and self.main.running_threads_on:

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
			#os.system('cls')
			speak("Exiting. Close Reaper's new version dialog box and restart Dawkside.",printout=True)
			os._exit(0)
		except ConnectionResetError:
			os.system('cls')
			speak("Exiting Reaper.",printout=True)
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
					self.plugins.index[1] = self.plugins.index[0]
					self.plugins.page[2] = self.plugins.page[0]
			
			if id != track.id:
				id = track.id
				self.switch_on = True
				changed = True
				self.switchtime = time.time()
			
			if self.plugins.index[1] != self.plugins.index[0] and time.time()-self.main.switchtime >= self.switch_delay:
				self.get_data(['fx'])
				self.plugins.index[1] = self.plugins.index[0]
				self.track.history[track.id]['fx'] = self.plugins.index[0]
			
			if self.plugins.page[2] != self.plugins.page[0] and time.time()-self.main.switchtime >= self.switch_delay:
				self.get_data(['fx'])
				self.plugins.page[2] = self.plugins.page[0]
				self.track.history[track.id]['pg'] = self.plugins.page[0]
		
		if changed:
			reset = 0
		else:
			reset += 1
		if reset > 15:
			
			# Check new sends
			sendTmp = track.n_sends
			recvTmp = track.n_receives
			if self.track.nsend != sendTmp or self.track.nrecv != recvTmp:
				self.get_data(['sendrecv'])
			self.track.nsend = int(sendTmp)
			self.track.nrecv = (recvTmp)
			
			# Check plugins list changes
			fxTmp = track.n_fxs
			if self.plugins.nfxs != fxTmp:
				self.get_data(['fx','plugins'])
			reset = 0
			
		time.sleep(0.1)