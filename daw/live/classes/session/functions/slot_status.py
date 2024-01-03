from functions.misc import invert_grid_position

def slot_status(self,args):
	""" Manages Live tracks clips information. """

	daw = self.daw
	track = args[1]
	slot = args[2]
	type = 'playing' if 'playing' in args[0] else 'fired'
	tracks = daw.tracks
	scenes = daw.scenes
	
	if track in tracks.tracks:
		tmp = tracks.tracks[track]
		if type == 'playing':
			
			if slot >= 0:
				tmp['playing'] = slot
				if tmp['clips'][slot]:
					pass
				else:
					daw.client.send_message('/live/clip/get/name',(track,slot))
			else:
				if slot == -2:
					tmp['playing'] = -1
			for _ in range(scenes.num):
				if tmp['clips'][_]:
					c = 'lcply' if _ == tmp['playing'] else 'lcact'
				else:
					c = 'off'
				for m in daw.online['control']:
					pos = invert_grid_position((track-m.exclusive['live']['track_offset'])+((_-m.exclusive['live']['scene_offset'])*8))
					m.matrix_in(pos[0],c,action='unit')
				
		if type == 'fired':
			
			if slot >= 0:
				if tmp['clips'][slot]:
					# color when an actual clip is being launched
					c = 'lcfir'
				else:
					# color when a new clip is to be recorded
					c = 'lcrw'
			else:
				c = 'yel' if tmp['playing'] else 'red'
			
			for m in daw.online['control']:
				pos = invert_grid_position((track-m.exclusive['live']['track_offset'])+((slot-m.exclusive['live']['scene_offset'])*8))
				m.matrix_in(pos[0],c,action='unit')