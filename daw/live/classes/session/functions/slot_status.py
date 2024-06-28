def slot_status(self,args):
	""" Manages Live tracks clips information. """

	daw = self.daw
	track = args[1]
	scene = args[2]
	if 'playing' in args[0]:
		action = 'playing'
	elif 'fired' in args[0]:
		action = 'fired'
	elif 'has_clip' in args[0]:
		action = 'clips'
	elif 'has_stop_button' in args[0]:
		action = 'stop_buttons'
	
	tracks = daw.tracks
	scenes = daw.scenes
	
	if track in tracks.tracks:
		tmp = tracks.tracks[track]
		
		if 'clips' in action or 'stop_buttons' in action:

			state = args[3]

			if state:

				if action == 'clips':
					daw.client.send_message('/live/clip/get/name',(track,scene))
			else:
				tmp[action][scene] = None
				for m in daw.online['control']:
					exclusive = m.daw_vars
					pos = (track-exclusive['track_offset'])+((scene-exclusive['scene_offset'])*8)
					m.matrix_in(pos+1000,'off',action='unit')

			"""
			for m in daw.online['control']:
					
					
			if state:
				if tmp[action][scene] != None:
					daw.client.send_message('/live/clip/get/name',(track,scene))
				else:
					tmp[action][scene] = None
				if action == 'stop_buttons':
					c = 'dim' if state else 'off'
			"""
		
		if action == 'playing':
			
			if scene >= 0:
				tmp['playing'] = scene
				if tmp['clips'][scene]:
					pass
				else:
					daw.client.send_message('/live/clip/get/name',(track,scene))
			else:
				if scene == -2:
					tmp['playing'] = -1
			for _ in range(scenes.num[0]):
				if tmp['clips'][_] != None:
					c = 'clip_playing' if _ == tmp['playing'] else 'clip_stopped'
				else:
					c = 'off'
				for m in daw.online['control']:
					exclusive = m.daw_vars
					pos = (track-exclusive['track_offset'])+((_-exclusive['scene_offset'])*8)
					m.matrix_in(pos+1000,c,action='unit')
				
		if action == 'fired':
			
			if scene >= 0:
				if tmp['clips'][scene]:
					# color when an actual clip is being launched
					c = 'clip_fired'
				else:
					# color when a new clip is to be recorded
					c = 'clip_fired'
			else:
				c = 'yel' if tmp['playing'] else 'red'
			
			for m in daw.online['control']:
				exclusive = m.daw_vars
				pos = (track-exclusive['track_offset'])+((scene-exclusive['scene_offset'])*8)
				m.matrix_in(pos+1000,c,action='unit')