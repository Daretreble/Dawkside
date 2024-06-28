import time
from functions.misc import invert_grid_position
from functions.speak import speak

class Clips:
	""" Manages Live's clips. """
	def __init__(self,daw):
		""" Manages Live's clips information. """
	
		self.daw = daw
		self.main = daw.main
		self.selected  = False
		self.loop_start = 0
		self.loop_end = 0
		
	def pad_trig(self,*args,**kwargs):
		""" Triggers defined clip """

		action = kwargs['action']
		daw = self.daw
		main = daw.main

		tracks = daw.tracks
		scenes = daw.scenes
		
		selected_track = args[0]
		selected_scene = args[1]

		if action == 'fire':
			
			daw.client.send_message('/live/clip_slot/fire',(selected_track,selected_scene))
				
		if action == 'delete':
			daw.client.send_message('/live/clip_slot/delete_clip',(selected_track,selected_scene))