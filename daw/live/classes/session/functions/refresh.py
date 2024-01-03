from functions.misc import invert_grid_position

def refresh(self,control):
	""" Refreshes Live's Session View. """

	daw = self.daw
	
	if daw.datatmp[2]:
	
		daw.get_data()
		
	else:

		tracks = daw.tracks
		scenes = daw.scenes
		
		if control:
			controls = [control]
		else:
			controls = daw.online['control']
		
		for m in controls:
		
			exclusive = m.exclusive['live']
			
			track_offset = exclusive['track_offset']
			scene_offset = exclusive['scene_offset']
			
			for track in range(8):
			
				if track+exclusive['track_offset'] < tracks.num:
					m.matrix_in(410+track,'smdon',action='unit')
					m.matrix_in(410+track,'mmdon',action='unit')
				else:
					m.matrix_in(410+track,'off',action='unit')
					m.matrix_in(410+track,'off',action='unit')
					
				
				for scene in range(8):
				
					pos = invert_grid_position(track+(scene*8))
					
					if track+track_offset >= tracks.num or scene+scene_offset >= scenes.num:
						c = 'lcnsb'
					else:
						tmp = tracks.tracks[track+track_offset]
						if tmp['clips'][scene+scene_offset]:
							if tmp['playing'] == scene+scene_offset:
								 c = 'lcply'
							else:
								c = 'lcact'
						else:
							if tmp['clips'][scene+scene_offset]:
								c = 'lcact'
							else:
								c = 'off'
								
						
					m.matrix_in(pos[0],c,action='unit')