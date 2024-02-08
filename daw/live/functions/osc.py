import time
from functions.misc import invert_grid_position,find_position,normalized_from_min_max
from functions.speak import speak

def osc(self,*args):
	""" Live OSC interpretation. """

	main = self.main
	tracks = self.tracks
	plugins = self.plugins
	scenes = self.scenes

	# Transport osc
	if args[0] in self.transport.osc_triggers:
		self.transport.osc_manage(args[0],args[1])
	
	if args[0] == '/live/startup':
		self.get_data()
	
	if args[0].startswith('/live/track/get/') and 'devices' not in args[0]:
		param_type = args[0].split('/')[-1]
		
		if param_type in self.triggers['track_toggle']:
			trig = self.triggers['track_toggle'][param_type]
			self.triggers['track_toggle'][param_type][2] = args[2]
			c = 'tr_play_on' if args[2] == trig[1] else 'tr_play_off'
			for m in self.online['control']:
				m.matrix_in(trig[0],c,action='unit')
			
		
		if param_type == 'name':
			self.track.name = args[2]

	
	if args[0] == '/live/view/get/selected_track':
		self.track.index[0] = args[1]
		self.datatmp['osc_tracking']['track_change'][1] = time.time()
		self.datatmp['osc_tracking']['track_change'][0] = True

	if args[0] == '/live/view/get/selected_scene':
		self.scenes.index[0] = args[1]
		self.client.send_message('/live/clip_slot/get/has_clip',(self.track.index[0],self.scenes.index[0]))
		speak(self.scenes.index[0])
	
	if args[0] == '/live/clip_slot/get/has_clip' and args[3] and args[1] == self.track.index[0] and args[2] == self.scenes.index[0]:
		main.play_sound('high')
	
	if args[0] == '/live/song/get/num_tracks':
		tracks.num = args[1]
		
	if args[0] == '/live/song/get/num_scenes':
		scenes.num = args[1]
	
	## Get devices data
	if args[0] == '/live/track/get/devices/name':
		self.devices_manage(*args,action='get_devices')
	
	if args[0] == '/live/device/get/parameters/name':
		self.devices_manage(*args,action='get_parameter_names')

	if args[0] == '/live/device/get/parameter/value':
		param_tmp = self.plugins.params[args[3]+1]
		value_out = normalized_from_min_max(args[4],param_tmp['min'],param_tmp['max']) 
		param_number = args[3]+1
		ids = self.fre['plugins']['ids']
		if param_number in plugins.params:
			plugins.params[param_number]['val'] = value_out
			if param_number in ids:
				for m in self.online['control']:
					for pos in ids[param_number]:
						m.fre_feedback(12,pos,value_out)
			if param_number in self.fre['plugins']['btns']:
				btns_tmp = self.fre['plugins']['btns'][param_number]
				
				for key,value in btns_tmp.items():
					state = True if  value[0] <= value_out else False
					
				if state != self.fre['plugins']['btns'][param_number][key][1]:
					# Action to trigger layout
					for m in self.online['control']:
						if key in m.matrix['plugin_buttons'][1]:
							for l in m.matrix['plugin_buttons'][1][key]:
								c = 'plugins_usrbtn_param_on' if state else 'plugins_usrbtn_param_off'
								m.matrix_in(l,c,action='unit',direct=True)

							self.fre['plugins']['btns'][param_number][key][1] = state
						
				
				"""state = True if  v <= value_out else False
					#print(p,state,self.fre['plugins']['btns'][param_number][count][2])
					if state != self.fre['plugins']['btns'][param_number][count][2]:
						# Action to trigger layouts
						

						self.fre['plugins']['btns'][param_number][count][2] = state
					
					count += 1
			"""

	if args[0] == '/live/device/get/parameter/value_string':
		#print(find_position(args[3]))
		param_tmp = self.plugins.params[args[3]+1]
		#print(param_tmp['name'])
		#speak(args[4])

	
	
	if args[0] == '/live/device/get/parameters/value':
		self.devices_manage(*args,action='get_parameter_values')

	if args[0] == '/live/device/get/parameters/min':
		self.devices_manage(*args,action='get_parameter_mins')

	if args[0] == '/live/device/get/parameters/max':
		self.devices_manage(*args,action='get_parameter_maxs')

	if args[0] == '/live/device/get/parameters/default_value':
		self.devices_manage(*args,action='get_parameter_defaultss')
		
		#track.index[0] = args[1]
	
	"""
	if args[0] == '/live/clip_slot/get/has_stop_button':
		tracks.tracks[args[1]]['stop_button'][args[2]] = args[3]
		if not args[3]:
			for m in self.online['control']:
				pos = invert_grid_position(args[1]+(args[2]*8))
				if pos[0] < 64:
					m.matrix_in(pos[0],'lcnsb',action='unit')
	
	
	
	if args[0] == '/live/clip/get/name':
		if tracks.tracks[args[1]]['clips'][args[2]]:
			pass
		else:
			tracks.tracks[args[1]]['clips'][args[2]] = args[3]
			for m in self.online['control']:
				pos = invert_grid_position((args[1]-m.exclusive['live']['track_offset'])+((args[2]-m.exclusive['live']['scene_offset'])*8))
				if pos[0] < 64:
					m.matrix_in(pos[0],'lcrec',action='unit')
	
	if args[0]== '/live/track/get/playing_slot_index':
		self.session.slot_status(args)
	
	if args[0]== '/live/track/get/fired_slot_index':
		self.session.slot_status(args)
	
	if args[0] == '/live/song/get/track_data':

		tracks.tracks = {}
		count1 = 0
		track=0
		for _ in args[1:]:
			if count1 % (scenes.num+1) == 0:
				scene=0
				tracks.tracks.update({track:{
					'name':_,
					'playing':-1,
					'fired':-1,
					'clips':[],
					'stop_button':[],
				}})
				track+=1
				### Remplir les stop buttons
			else:
				tracks.tracks[track-1]['clips'].append(_)
				tracks.tracks[track-1]['stop_button'].append(None)
				self.client.send_message('/live/clip_slot/get/has_stop_button',(track-1,scene))
				scene+=1
			count1+=1
		self.datatmp[3] = False
		self.tracks.num = track
		self.scenes.num = scene
		time.sleep(1)
		#self.session.refresh(False)
			
	
	if args[0] == '/live/view/get/selected_scene':
		scenes.selected = args[1]
		time.sleep(0.5)
		self.speak(scenes.selected)
		
	if args[0] == '/live/device/get/parameter/value':
		speak(round(args[4],3))
	
	

	"""