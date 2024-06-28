from functions.speak import speak

def scroll(self,control,*args,**kwargs):
	""" Scrolls around Live's Session View tracks and scenes. """

	id = args[0]
	exclusive = control.exclusive[self.daw.short_name]
	
	if id == 440 and exclusive['track_offset'] != 0:
		exclusive['track_offset'] -= 1
	if id == 441:
		exclusive['track_offset'] += 1
	if id == 442 and exclusive['scene_offset'] != 0:
		exclusive['scene_offset'] -= 1
	if id == 443:
		exclusive['scene_offset'] += 1
	self.refresh(control)
	speak(f"{exclusive['track_offset']} {exclusive['scene_offset']}")