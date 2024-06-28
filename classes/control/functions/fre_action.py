import os
from functions.speak import speak

def fre_action(self,info):
	""" Actions on fre touch. """

	daw = self.daw
	main = daw.main
	plugins = daw.plugins
	
	if plugins.act:
	
		action = info[3]
		pos = info[0][0]
		state = info[1]
		sn = daw.short_name
		
		outmode = self.daw_vars['outmode']

		if action in['add_param','delete_param']:
			
			## Add selected parameter to fader
			if action == 'add_param' and state:
				daw.plugins.user.param_set(pos,'add')

			## Delete selected parameter to fader
			if action == 'delete_param' and state:
				daw.plugins.user.param_set(pos,'delete')

		else:
		
			fre_tmp = False
			
			# Track faders
			if outmode == 11:
				if pos < 6:
					fre_tmp = daw.fre['track'][self.daw_vars['sendrecv']['selected']]
				else:
					fre_tmp = daw.fre['track']['track']

			# Plugins faders
			if outmode == 12:
				try:
					fre_tmp = daw.fre['plugins']['faders']
				except KeyError:
					print('fre_actions line 51')

			if fre_tmp and pos in fre_tmp:
				
				fader_name = fre_tmp[pos]['name']
				if outmode in[11]:
					fader_value = fre_tmp[pos]['valstr']
				if outmode == 12:
					fader_value = daw.plugins.params[fre_tmp[pos]['prm']]['valstr']

				## Defaults
				if action == 'default' and state:

					default_value = False
					
					if outmode == 11:
						if pos < 6:
							if self.daw_vars['sendrecv']['selected'] == 'send':
								
								# Send default value
								if sn == 'reaper':
									default_value = [0.716,f"/track/send/{pos+1}/volume"]
							
							if self.daw_vars['sendrecv']['selected'] == 'recv':
								
								# Receive default value
								if sn == 'reaper':
									default_value = [0.716,f"/track/recv/{pos+1}/volume"]
						else:
							if pos == 6:
								
								# Pan default value
								if sn == 'reaper':
									default_value = [0.5,'/track/pan']
							
							if pos == 7:
								
								# Voume default value
									if sn == 'reaper':
										default_value = [0.716,'/track/volume']

					if outmode == 12:
						default_value = [daw.plugins.params[fre_tmp[pos]['prm']]['defval'],f"/fxparam/{fre_tmp[pos]['prm']}/value"]
						
					if default_value:
						value_out = default_value[0]
						osc_msg = default_value[1]
						daw.client.send_message(osc_msg,value_out)
						for m in daw.online['control']:
							m.fre_feedback(outmode,pos,value_out)
						speak(f"{fader_name} resetted to defaults")
				

				## Output
				if action == 'output':
					if state:
						speak(fader_name)
					else:
						if fader_value != '':
							speak(fader_value)
			else:
				if state:
					speak("Empty")

	else:
		speak("Please add a plugin.")