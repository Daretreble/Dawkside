import os
import pprint
import copy
import time
from functions.misc import model_rotary_menus
from functions.speak import speak

def command_common(self,control,id,info,options):
	""" Sends common commands for all daws. """

	main = self.main
	plugins = self.plugins
	modif = main.modif
	help = modif('test',[911])
	state = info[1]
	mode = control.daw_vars['mode']
	outmode = control.daw_vars['outmode']
	passed = True
	params = options['params'] if 'params' in options else False

	if '--show-id' in main.queries:
		print(id,state)
	
	## Debug
	if state and id == 999:
		os.system('cls')
		pprint.pprint(self.tracks.tracks)

	## All modifiers
	if id not in range(921,924) and id in main.modifiers_data['list']:
		modif('trig',id,state)
	
	## (200-207) Faders and encoders output
	if id in range(200,232):
		pos = id-200
		if modif('test',[910]) and plugins.act:
			self.plugins.user.param_set(pos,'add')
		else:
			control.fre_process(info)

	## Encoder 1
	if state and id == 251:
		rotary_info = model_rotary_menus(info)
		output_type = options['type']
		
		if output_type == 'param_nav':
			plugins.param_nav((1*rotary_info[1]) if rotary_info[0] else (-1*rotary_info[1]),action='nav')
		if output_type == 'scale_nav':
			control.modes.scales_nav(1 if rotary_info[0] else -1,action='nav')
		if output_type == 'scene_nav':
			self.scenes.select((1*rotary_info[1]) if rotary_info[0] else (-1*rotary_info[1]),action='nav')
	
	## Daw select
	if state and id in range(420,425) and id-420 < len(main.daws):
		pass

	## Modes select
	if state and id in range(400,408) and id-300 in self.modes:
		if help:
			speak(f"Select the {self.modes[id-300]['name']} mode for {self.name}. {self.modes[id-300]['desc']}")
		else:
			control.mode_select(mode=[1,id-300],speak=True)

	## Play modes select
	if state and id in range(430,438) and id-300 in control.modes.sections:
		if help:
			speak(f"Select the {control.modes.sections[id-300]['name']} control mode. {control.modes.sections[id-300]['desc']}")
		else:
			control.mode_select(mode=[1,id-300],speak=True)

	## Play modes trigger
	if mode in range(130,138):
		if id in range(800,864):
			control.modes.sections[mode]['class'].trig(id,info)
		if state and id in range(864,868):
			action = 'reset' if modif('test',[900]) else 'transpose'
			control.modes.transpose(id,info,action)
		if state and id in[868,869]:
			control.modes.scales_nav(1 if id == 869 else -1,action='nav')

	## Output mode select
	if state and id in range(410,415) and id-400 in main.outmodes:
		if help:
			speak(f"Select the {main.outmodes[id-400]['name']} output mode. {main.outmodes[id-400]['desc']}")
		else:
			control.mode_select(mode=[2,id-400],speak=True)

	## Daw select
	if state and id in range(420,425):
		control.settings['selected_daw'] = main.daws_index[420-id]
		control.daw_prepare()
	
	## Transport
	if (params or state) and id in self.transport.triggers:
		if help:
			self.transport.help(id)
		else:
			self.transport.trig(id,params)
	"""
	if id in self.transport['trig']:
		transport(self,id,info,action='trig')
	"""
	
	## Send Receive selection
	if state and id in[120,121]:
		self.track.send_recv_select(control,id)

	## Plugin page type selection
	if id in[380,381] and state:
		plugins.type_select(id)
	
	# Plugins Parameters nav
	if id in[382,383] and state:
		plugins.param_nav(1 if id == 383 else -1,action='nav')
	
	## Plugins Page nav
	if id in[376,377] and state:
		if modif('test',[910,900]):
			plugins.user.page_rename()
		elif modif('test',[909]):
			plugins.user.page_add_delete(action='delete')
		elif modif('test',[910]):
			plugins.user.page_add_delete(action='add')
		else:
			plugins.page_nav('nav',-1 if id == 376 else 1)

	## Plugin nav
	if id in range(360,376) and state:
		plugins.plugin_nav('select',id)
	if state and id in[378,379]:
		dir = -1 if id == 378 else 1
		plugins.plugin_nav('nav',dir)
	
	## User page buttons
	if id in range(260,292):
		if modif('status')[0]:
			if state and modif('test',[910]):
				control.buttons.edit(button_type='plugin_button', pos=id-260)
			elif state and modif('test',[909]):
				control.buttons.delete(button_type='plugin_button', pos=id-260)
			#main.switchtime = time.time()
		elif time.time() - main.switchtime > 0.5:
			control.buttons.exec(button_type='plugin_button', pos=id-260, velocity=info[2], state=info[1])
	
	## Faders and encoders actions
	if id in range(300,308):
		if help:
			if state:
				speak("Faders and encoders buttons: Employ these buttons to efficiently control different aspects of a fader or encoder, such as associated parameters and customization options.")
		else:
			info_tmp = copy.deepcopy(info)
			info_tmp[0][0] = id-300
			# Initializes to defaults
			if modif('test',[900]):
				info_tmp.append('default')
			# Add selected parameter to fre
			elif modif('test',[910]) and outmode == 12:
				info_tmp.append('add_param')
			elif modif('test',[909]) and outmode == 12:
				info_tmp.append('delete_param')
			else:
				# Output name and value
				info_tmp.append('output')
			if len(info_tmp) == 4:
				control.fre_action(info_tmp)

	## Keys management buttons
	if state and id == 706 and control.keys_assoc.act:
		if modif('test',[909]):
			control.keys_assoc.zone_manage(False,action='pluginzoneclear')
		else:
			control.keys_assoc.zone_manage(False,action='pluginzonesave')

	for inc in[0,10]:
		dir = 1 if inc == 10 else -1
		toggle = True if inc == 10 else False
		if state and id in range(700+inc,704+inc):
			if control.keys_assoc.act:
				if modif('test',[909,910]):
					control.keys_assoc.zone_manage(False,action='trackzonesave')
				elif modif('test',[900]):
					control.keys_assoc.zone_manage(id-(700+inc),toggle,action='zonesustain')
				elif modif('test',[909]):
					control.keys_assoc.zone_manage(id-(700+inc),action='zonetransposereset')
				elif modif('test',[910]):
					control.keys_assoc.zone_manage(id-(700+inc),dir,action='zonechannel')
				else:
					control.keys_assoc.zone_manage(id-(700+inc),dir,action='zonetranspose')
			else:
				speak(control.keys_assoc.name+" is currently unavailable. Please ensure that the keys controller is not already activated within the selected DAW.")
	## Routing functions
	if state and id == 752:
		control.daw_routing(daw='reaper',speak=True)

	if state and id == 750:
		control.daw_routing(speak=True)

	if state and id == 751:
		if 'destination' not in options:
			speak("No destination key in dictionnary")
		elif options['destination'] not in main.devices['ports']:
			speak("That port is not created.")
		else:
			control.keys_assoc.routing_destination = main.devices['ports'][options['destination']].port
			control.keys_assoc.panic()
			speak("Keys routed to "+main.devices['ports'][options['destination']].name)
	
	self.command_launch(control,id,info,options)