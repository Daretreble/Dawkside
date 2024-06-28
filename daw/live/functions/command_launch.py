import time
from threading import Thread
from functions.misc import find_position
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

	## previous and next track
	if state and id in[105,106]:
		dir = -1 if id == 105 else 1
		self.track_select(dir,action='nav')

	## previous and next scene
	if state and id in[1105,1106]:
		dir = -1 if id == 1105 else 1
		self.scenes.select(dir,action='nav')
	
	## 64 pads session grid
	if state and id in range(1000,1064):
		pos = find_position(id-1000)
		exclusive = control.daw_vars
		if modif('test',[911]):
			action = 'info'
		elif modif('test',[909]):
			action = 'delete'
		else:
			action = 'fire'
		self.clips.pad_trig(pos[0]+exclusive['track_offset'],pos[1]+exclusive['scene_offset'],action=action)
	
	## Selected clip actions
	if state and id == 1090:
		self.clips.pad_trig(self.track.index[0],self.scenes.index[0],action='delete')
	if state and id == 1091:
		self.clips.pad_trig(self.track.index[0],self.scenes.index[0],action='fire')

	## Reloads devices on selected track
	if state and id == 1198:
		self.client.send_message('/live/track/get/devices/name',(track.index[0]))
		speak("Reloaded")
	
	## Reloads Ableton OSC
	if state and id == 1199:
		speak("Ableton OSC API is reloading.")
		self.get_data()