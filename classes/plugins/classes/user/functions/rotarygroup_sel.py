from mido import Message as MidiMsg

def rotarygroup_sel(self,control,**kwargs):
	""" Select sub banks of faders, rotaries and encoders. """
	
	plugins = self.plugins
	daw = plugins.daw
	main = plugins.main
	
	action = kwargs['action']
	group = control.daw_vars['rotary_group']
	
	if action in['stepup','stepdown']:
		dir = 1 if action == 'stepup' else -1
		control.rotary_group+=dir
		if control.rotary_group > 4:
			control.rotary_group = 1
		if control.rotary_group < 1:
			control.rotary_group = 4
	
	if kwargs['speak']:
		Speak(control.row_def[control.rotary_group])
		
	if action in['refresh','stepdown','stepup']:
	
		if plugins.act and len(daw.fre['plugins']['faders']) > 0:
		
			if plugins.page_type == 0:
			
				if self.is_saved('page'):
					tmp = plugins.user_params[plugins.name][plugins.page[0]]['data']
					base = (control.daw_vars['rotary_group']-1) * 8
					for _ in range(control.fre_count):

						if _+base in tmp:
							c = 'fre_param_on'
							output_pitch = daw.fre['plugins']['faders'][_]['pitch'][0]
						else:
							c = 'fre_param_off'
							output_pitch = 0.0
						if control.daw_vars['outmode'] == 12:
							control.matrix_in(_+300,c,action='unit')
						control.fre_feedback(12,_,output_pitch)
							
			if plugins.page_type == 1:
			
				for _ in range(8):
					c = 'fre_param_on' if _ in daw.fre['plugins']['faders'] else 'fre_param_off'
					output_pitch = daw.fre['plugins']['faders'][_]['pitch'][0] if _ in daw.fre['plugins']['faders'] else 0.0
					if control.daw_vars['outmode'] == 12:
						control.matrix_in(_+300,c,action='unit')
					control.fre_feedback(12,_,output_pitch)
							
		else:
		
			for _ in range(8):
				if control.daw_vars['outmode'] == 12:
					control.matrix_in(_+300,'fre_param_off',action='unit')
				control.fre_feedback(12,_,0.0)