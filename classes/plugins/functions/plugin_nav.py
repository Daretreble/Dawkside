import time
from functions.speak import speak

def plugin_nav(self,action,*args):
	""" Navigates through plugins. """
	daw = self.daw
	main = self.main
	modif = main.modif

	if self.act:

		if action == 'select':
			index_tmp = args[0]-359
			if index_tmp <= self.nfxs:
				if modif('test',[911]):
					speak(f"Loads {self.plugins_list[index_tmp-1]}.")
				else:
					self.index[0] = index_tmp
					speak(f"{self.index[0]} {self.plugins_list[self.index[0]-1]}")
					if daw.short_name == 'reaper':
						if daw.reapy_mode:
							main.switchtime = time.time()
					if daw.short_name == 'live':
						daw.client.send_message('/live/track/get/devices/name',(daw.track.index[0],0))
			else:
				output = f"Button {index_tmp} in the group designed for loading a plugin on the track, even though this particular button contains no plugin." if modif('test',[911]) else "Empty."
				speak(output)
		if action == 'nav':
			dir = args[0]
			nfxs = self.nfxs
			if modif('test',[911]):
				if dir == 1:
					output = "Load the next plugin in the sequence."
				else:
					output = f"Load the previous plugin in the sequence."
				speak(output)
			else:
				if nfxs == 1:
					speak(f"{self.name} stands alone as the sole plugin gracing this track; there are no other plugins to traverse.")
				elif daw.short_name == 'reaper' and daw.reapy_mode == False:
					if self.index[0]+dir >= 1:
						self.index[0]+=dir
						daw.client.send_message('/device/fxparam/count',0)
						daw.client.send_message('/device/fx/select',self.index[0])
						daw.switchtime = time.time()
						daw.pVar = ['trackreload','plugin_select']
					else:
						speak(self.name+" nothing before.")
				elif self.index[0] + dir in range(1,self.nfxs+1):
					self.index[0]+=dir
					speak(f"{self.index[0]} {self.plugins_list[self.index[0]-1]}")
					
					if daw.short_name == 'reaper':
						main.switchtime = time.time()
					
					if daw.short_name == 'live':
						daw.client.send_message('/live/track/get/devices/name',(daw.track.index[0],0))
	else:
		speak("Insert a plugin onto your track to enable plugin's navigation.")