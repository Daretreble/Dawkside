import time
from threading import Thread
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

	## previous and next track
	if state and id in[105,106]:
		dir = -1 if id == 105 else 1
		self.track_select(dir,action='nav')

	## previous and next scene
	if state and id in[1105,1106]:
		dir = -1 if id == 1105 else 1
		self.scenes.select(dir,action='nav')
	
	## Manage cells
	if state and id == 1070:
		pos = options['pos']
		if modif('test',[900]):
			print('shirt',pos)
		else:
			def delayed_fire():
				time.sleep(0.2)
				self.client.send_message('/live/clip_slot/fire',(pos,self.scenes.index[0]))
			if self.track.index[0] != pos:
				Thread(target=delayed_fire).start()
				self.client.send_message('/live/view/set/selected_track',pos)
			else:
				self.client.send_message('/live/clip_slot/fire',(pos,self.scenes.index[0]))
			

	## Deletes selected clip
	if state and id == 1090:
		self.clips.delete(self.track.index[0],self.scenes.index[0])

	## Reloads devices on selected track
	if state and id == 1198:
		self.client.send_message('/live/track/get/devices/name',(track.index[0]))
		speak("Reloaded")
	
	## Reloads Ableton OSC
	if state and id == 1199:
		speak("Ableton OSC API is reloading.")
		self.get_data()