import time
from functions.misc import invert_grid_position
from functions.speak import speak

class Clips:
	""" Manages Live's clips. """
	def __init__(self,daw):
		""" Manages Live's clips information. """
	
		self.daw = daw
		self.selected  = False
		
	def delete(self,*args):
		""" Deletes selected clip """

		self.daw.client.send_message('/live/clip_slot/delete_clip',(args[0],args[1]))

	def trig(self,*args):
		""" Deletes selected clip """

		self.daw.client.send_message('/live/clip_slot/delete_clip',(args[0],args[1]))
	
	def pad_trig(self,*args,**kwargs):
		""" Triggers defined clip """

		action = kwargs['action']
		daw = self.daw
		main = daw.main

		tracks = daw.tracks
		scenes = daw.scenes
		
		selected_track = args[0]
		selected_scene = args[1]
		
		if selected_track < tracks.num and selected_scene < scenes.num:
			
			tmp = tracks.tracks[selected_track]
			
			if action == 'fire':
			
				if not tmp['clips'][selected_scene]:
					daw.tracks.setarm(selected_track)
					time.sleep(0.01)
				daw.client.send_message('/live/clip_slot/fire',(selected_track,selected_scene))
				
			if action == 'delete':
				if tmp['clips'][selected_scene]:
					daw.client.send_message('/live/clip_slot/delete_clip',(selected_track,selected_scene))
					tmp['clips'][selected_scene] = None
					for m in daw.online['control']:
						exclusive = m.exclusive['live']
						pos = invert_grid_position((selected_track-exclusive['track_offset'])+((selected_scene-exclusive['scene_offset'])*8))
						m.matrix_in(pos[0],'off',action='unit')
			
			if action == 'info':
				if tmp['clips'][selected_scene]:
					speak(tmp['clips'][selected_scene])
				else:
					speak('No Clip')
				
		else:
			speak('Out of range')