import random
from functions.speak import speak

def osc(self,*args):
	""" Reaper's OSC bride """
	
	main = self.main
	plugins = self.plugins

	# Transport osc
	if args[0] in self.transport.osc_triggers:
		self.transport.osc_manage(args[0],args[1])
	
	## Tempo
	if args[0] == '/tempo/str':
		speak(args[1])
	
	## Track osc
	
	# Get track's volume
	if args[0] == '/track/volume':
		value_out = round(args[1],4)
		self.fre['track']['track'][7]['pitch'] = [value_out,False]
		if not self.switch_on:
			for m in self.online['control']:
				m.fre_feedback(11,7,value_out)
	# Get track's volume value string
	if args[0] == '/track/volume/str':
		self.fre['track']['track'][7]['valstr'] = args[1]
		
	# Get track's pan
	if args[0] == '/track/pan':
		
		value_out = round(args[1],4)
		self.fre['track']['track'][6]['pitch'] = [value_out,False]
		if not self.switch_on:
			for m in self.online['control']:
				m.fre_feedback(11,6,value_out)
		
	# Get pan's value string
	if args[0] == '/track/pan/str':
		self.fre['track']['track'][6]['valstr'] = args[1]
	
	# Get Send Receive data
	if args[0][:12] in['/track/send/','/track/recv/']:
		sr_type = args[0][7:11]
		sr_tags = args[0][12:].split('/')
		sr_id = int(sr_tags[0])
		
		if sr_id-1 in self.fre['track'][sr_type]:
			
			if len(sr_tags) == 3:
				sr_cat = sr_tags[1]+'/'+sr_tags[2]
			else:
				sr_cat = sr_tags[1]
			if sr_cat == 'volume':
				value_out = round(args[1],4)
				self.fre['track'][sr_type][sr_id-1]['pitch'] = [value_out,False]
				if not self.switch_on:
					for m in self.online['control']:
						send_recv_sel = m.daw_vars['sendrecv']['selected']
						if send_recv_sel == sr_type:
							m.fre_feedback(11,sr_id-1,value_out)
				
			if sr_cat == 'volume/str':
				self.fre['track'][sr_type][sr_id-1]['valstr'] = args[1]
		
	## Plugins osc
	
	# Get parameter  valuees
	if args[0].startswith('/fxparam'):
		zones = args[0].split('/')
		
		if zones[2] == 'last_touched':
			pass
		else:
			param_number = int(zones [2])
			
			if zones[3] == 'value':
				ids = self.fre['plugins']['ids']
				if len(zones) == 5:
					prm = int(zones[2])
					if zones[4] == 'str' and prm in plugins.params:
						plugins.params[prm]['valstr'] = args[1]
				else:
					value_out = round(args[1],4)
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