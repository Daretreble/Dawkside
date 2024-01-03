import pprint

def refresh(self,*args,**kwargs):

	control = self.control
	daw = self.control.daw
	main = daw.main
	plugins = daw.plugins
	user = plugins.user

	pos = args[0]
	button = args[1]
	c = False

	if 'event' not in kwargs:
		button = args[1]['pressed'][0] if 'pressed' in args[1] else args[1]['released'][0] if 'released' in args[1] else False
		
		if button:
			
			event_type = button['event_type']

			# Command
			if event_type == 'command':

				command_id = button['id']
				
				if command_id in control.refer_colors:
					c = control.refer_colors[command_id]
			
			# Plugin parameter
			if event_type == 'plugin_param':

				param_id = button['param_id']
				on_value = button['value']
				actual_value =  plugins.params[param_id]['val']
				state = True if  on_value <= actual_value else False

				c = 'plugins_usrbtn_param_on' if state else 'plugins_usrbtn_param_off'

			if event_type == 'midi_note':
				
				c = 'plugins_usrbtn_nt_off'
			
			if c:
				control.matrix_in(pos,c,action='unit',direct=True)