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

	if state and id == 104:
		self.client.send_message('/live/song/tap_tempo',())