from functions.speak import speak
from functions.speak import speak

def command_launch(self,control,id,info,options):
	""" Live's Command actions. """

	main = self.main
	modif = main.modif
	track = self.track
	state = info[1]
	mode = control.daw_vars['mode']

	## Trigger track toggles
	if state and id in self.triggers['track_toggle_ids']:
		trig = self.triggers['track_toggle'][ self.triggers['track_toggle_ids'][id] ]
		new_state = False if trig[2] else True
		self.client.send_message('/live/track/set/'+self.triggers['track_toggle_ids'][id],(track.index[0],new_state))
		
	## Undo
	if state and id == 80:
		self.client.send_message('/live/song/undo',())

	## Redo
	if state and id == 81:
		self.client.send_message('/live/song/redo',())

	## Tap tempo
	if id == 104:
		if state:
			c = 'tr_play_on'
			self.client.send_message('/live/song/tap_tempo',())
		else:
			c = 'tr_play_off'
		control.matrix_in(id,c,action='unit')

	## Reloads Ableton OSC
		if state and id == 1199:
			self.client.send_message('/live/api/reload',())
			speak("Ableton OSC API is reloading.")