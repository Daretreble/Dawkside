from functions.speak import speak

def type_select(self,*args):
	""" Page type selection. """
	daw = self.daw
	main = daw.main
	modif = main.modif
	
	page_type = args[0]-380

	if self.act:
		
		if page_type == 0:
			output=  "Choose the User Page type. In this mode, you have the freedom to craft personalized pages for your plugins, complete with unique settings for every fader or encoder, as well as a variety of custom-defined buttons."
		else:
			output = "Opt for the 8-Banks page type. In this mode, you'll find standard pages featuring 8 parameters neatly arranged in the order of the plugin's parameter list, along with predefined buttons for added convenience."


		if modif('test',[911]):
			speak(output)
		else:
			self.page_type = page_type
			if daw.short_name == 'reaper':
				daw.pVar = ['fxreload']
			if daw.short_name == 'live':
				daw.client.send_message('/live/track/get/devices/name',(daw.track.index[0],0))
			speak('8-Banks' if self.page_type == 1 else 'User page')
	else:
		speak("Insert a plugin onto your track to enable the selection of a page type.")