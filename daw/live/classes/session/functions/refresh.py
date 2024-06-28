def refresh(self,control):
	""" Refreshes Live's Session View. """

	daw = self.daw
	
	if False:
	
		daw.get_data()
		
	else:

		tracks = daw.tracks
		scenes = daw.scenes

		if control:
			controls = [control]
		else:
			controls = daw.online['control']
		
		for m in controls:
		
			exclusive = m.daw_vars

			track_offset = exclusive['track_offset']
			scene_offset = exclusive['scene_offset']
			
			for track in range(8):
			
				"""
				if track+exclusive['track_offset'] < tracks.num[0]:
					m.matrix_in(410+track,'smdon',action='unit')
					m.matrix_in(410+track,'mmdon',action='unit')
				else:
					m.matrix_in(410+track,'off',action='unit')
					m.matrix_in(410+track,'off',action='unit')
				"""
				
				for scene in range(8):
				
					pos = track+(scene*8)
					
					if track+track_offset >= tracks.num[0] or scene+scene_offset >= scenes.num[0]:
						c = 'off'
					else:
						tmp = tracks.tracks[track+track_offset]
						if tmp['clips'][scene+scene_offset] != None:
							if tmp['playing'] == scene+scene_offset:
								c = 'clip_playing'
							else:
								c = 'clip_stopped'
						else:
							if tmp['clips'][scene+scene_offset]:
								c = 'on'
							else:
								c = 'off'
								
						
					m.matrix_in(pos+1000,c,action='unit')