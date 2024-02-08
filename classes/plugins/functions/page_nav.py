import time
from functions.speak import speak

def page_nav(self,action,*args):
	""" Plugins page management. """	
	
	user = self.user
	daw = user.plugins.daw
	main = self.main
	modif = main.modif
	
	if self.act:
		if action == 'select':
			self.page[0] = args[0]
		if action == 'nav':
			if modif('test',[911]):
				if args[0] == 1:
					output = f"Go to next page."
				else:
					output = f"Go to previous page."
				speak(output)
			else:
				if self.page[0] + args[0] >= 1:
					self.page[0]+=args[0]
				if self.page_type == 0:
					if user.is_saved('page'):
						self.page[1] = self.user_params[self.name][self.page[0]]['page_name']
						if self.page[1] == '':
							speak(f"Page {self.page[0]}")
						else:
							speak(self.page[1])
					else:
						speak(f"Empty page {self.page[0]}")
				if self.page_type == 1:
					base = ((self.page[0]-1)*8) + 1
					if base in self.params:
						speak(f"{self.params[base]['name']}")
					else:
						speak("Out of range")
				
				if daw.short_name == 'reaper':
					if daw.reapy_mode:
						main.switchtime = time.time()
					else:
						daw.pVar = ['page_change']
						daw.switchtime = time.time()

				if daw.short_name == 'live':
					daw.datatmp['osc_tracking']['page_change'][1] = time.time()
					daw.datatmp['osc_tracking']['page_change'][0] = True
					#daw.client.send_message('/live/track/get/devices/name',(daw.track.index[0],0))
				
	else:
		speak("Insert a plugin onto your track to enable page selection.")
