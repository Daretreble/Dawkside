import time
import os
import pprint
from functions.misc import invert_grid_position,find_position,normalized_from_min_max
from functions.speak import speak

def osc(self,*args):
	""" Live OSC interpretation. """

	main = self.main
	tracks = self.tracks
	plugins = self.plugins
	scenes = self.scenes

	if 'error' in args[0]:
		pass
		#print(args)
	
	if args[0]== '/live/startup':
		pass
		#self.client.send_message('/live/song/get/track_data',(0,self.tracks.num[0],'track.name','clip.name'))

	if args[0] == '/live/track/get/send':
		value_out = round(args[3],4)
		self.fre['track']['send'][args[2]] = {
			'name': 'Send '+str(args[2]),
			'pitch': [value_out,False],
			'valstr':str(round(value_out)*100)
			}
		for m in self.online['control']:
			m.fre_feedback(11,args[2],value_out)
	
	if args[0] == '/live/track/get/name':
		self.track.name = args[2]

	if args[0] == '/live/track/get/volume':
		value_out = round(args[2],4)
		self.fre['track']['track'][7]['pitch'] = [value_out,False]
		for m in self.online['control']:
			m.fre_feedback(11,7,value_out)

	if args[0] == '/live/track/get/panning':
		value_out = round(args[2]+0.5,4)
		self.fre['track']['track'][6]['pitch'] = [value_out,False]
		for m in self.online['control']:
			m.fre_feedback(11,6,value_out)

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
		self.loop_switchtime = time.time()
		self.track.index[0] = args[1]
		self.client.send_message('/live/clip_slot/get/has_clip',(self.track.index[0],self.scenes.index[0]))
		self.datatmp['osc_tracking']['track_change'] = [True,time.time()]

	if args[0] == '/live/view/get/selected_scene':
		self.scenes.index[0] = args[1]
		self.client.send_message('/live/clip_slot/get/has_clip',(self.track.index[0],self.scenes.index[0]))
		self.datatmp['osc_tracking']['scene_change'] = [True,time.time()]
	
	if args[0] == '/live/clip_slot/get/has_clip':
		pass
		#self.session.slot_status(args)
		"""
		selected_scene_output = str(self.scenes.index[0]+1)
		if args[3]:
			speak(selected_scene_output+' clip')
		else:
			speak(selected_scene_output+' empty')
		"""
	
	## Get selected track
	if args[0] == '/live/song/get/num_tracks':
		tracks.num[0] = args[1]
		if tracks.num[1] != args[1]:
			#self.client.send_message('/live/song/get/track_data',(0,self.tracks.num[0],'track.name','clip.name'))
			#time.sleep(0.2)
			#for _ in range(tracks.num[0]):
				#self.client.send_message('/live/track/start_listen/playing_slot_index',(_))
				#self.client.send_message('/live/track/start_listen/fired_slot_index',(_))
			tracks.num[1] = args[1]

	## Get selected scene
	if args[0] == '/live/song/get/num_scenes':
		scenes.num[0] = args[1]
		if scenes.num[1] != args[1]:
			#self.client.send_message('/live/song/get/track_data',(0,self.tracks.num[0],'track.name','clip.name'))
			scenes.num[1] = args[1]
	
	## Get devices data
	if args[0] == '/live/track/get/devices/name':
		if time.time() - self.datatmp['osc_tracking']['devices_check'][1] > 1:
			if 'devices_check' in self.pVar:
				plugins_tmp = []
				for device in args[2:]:
					plugins_tmp.append([device])
				if not plugins_tmp == plugins.plugins_list:
					self.devices_manage(*args,action='get_devices')
					speak("Plugins list updated.")
				self.pVar = []
			else:
				self.devices_manage(*args,action='get_devices')
			self.datatmp['osc_tracking']['page_change'][1] = time.time()
		else:
			pass
			### DEV
			#print('deadly repeat')
	
	if args[0] == '/live/device/get/parameters/name':
		self.devices_manage(*args,action='get_parameter_names')

	if args[0] == '/live/device/get/parameter/value':
		param_tmp = self.plugins.params[args[3]+1]
		value_out = normalized_from_min_max(args[4],param_tmp['min'],param_tmp['max'])
		param_number = args[3]+1
		ids = self.fre['plugins']['ids']
		if param_number in plugins.params:
			plugins.params[param_number]['val'] = value_out
			if param_number in ids and not self.datatmp['osc_tracking']['page_load'][0]:
				for m in self.online['control']:
					for pos in ids[param_number]:
						m.fre_feedback(12,pos,value_out)
			if param_number in self.fre['plugins']['btns'] and not self.datatmp['osc_tracking']['page_load'][0]:
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

	if args[0] == '/live/device/get/parameter/value_string':
		plugins.params[args[3]+1]['valstr'] = args[4]

	if args[0] == '/live/device/get/parameters/min':
		self.devices_manage(*args,action='get_parameter_mins')

	if args[0] == '/live/device/get/parameters/max':
		self.devices_manage(*args,action='get_parameter_maxs')

	if args[0] == '/live/device/get/parameters/default_value':
		self.devices_manage(*args,action='get_parameter_defaultss')
		
		#track.index[0] = args[1]
	
	if args[0] == '/live/song/get/track_data':
		tracks.tracks = {}
		count1 = 0
		track=0
		scene = 0
		for _ in args[1:]:
			if count1 % (scenes.num[0]+1) == 0:
				scene=0
				tracks.tracks.update({track:{
					'name':_,
					'playing':-1,
					'fired':-1,
					'clips':[],
					'stop_button':[],
				}})
				track+=1
			else:
				tracks.tracks[track-1]['clips'].append(_)
				tracks.tracks[track-1]['stop_button'].append(None)
				#self.client.send_message('/live/clip_slot/start_listen/has_stop_button',(track-1,scene))
				#self.client.send_message('/live/clip_slot/start_listen/has_clip',(track-1,scene))
				scene+=1
			count1+=1
		self.tracks.num[0] = track
		self.scenes.num[0] = scene
		#time.sleep(0.1)
		#self.session.refresh(False)
			
	#if args[0]== '/live/track/get/playing_slot_index':
		#self.session.slot_status(args)
	
	#if args[0]== '/live/track/get/fired_slot_index':
		#self.session.slot_status(args)

	if args[0] == '/live/clip/get/name':
		if tracks.tracks[args[1]]['clips'][args[2]]:
			pass
		else:
			tracks.tracks[args[1]]['clips'][args[2]] = args[3]
			c = 'clip_playing' if tracks.tracks[args[1]]['playing'] == args[2] else 'clip_stopped'
			for m in self.online['control']:
				exclusive = m.daw_vars
				pos = (args[1]-exclusive['track_offset'])+((args[2]-exclusive['scene_offset'])*8)
				if pos < 64:
					m.matrix_in(pos+1000,c,action='unit')
	
	if 'has_stop_button' in args[0]:
		pass
		#print(args)
	
	if args[0] == '/live/clip/get/loop_start':
		pass
		#print(args)

	if args[0] == '/live/clip/get/loop_end':
		pass
		#print(args)