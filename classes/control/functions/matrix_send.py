import copy
import pprint
import os
from functions.command_common import command_common
from functions.misc import update_multi_level_dict
from functions.speak import speak
from threading import Thread

def matrix_send(self,info):
	""" Dispatches control buttons to commands. """
	
	daw = self.daw
	main = daw.main
	modif = main.modif
	
	id = info[0][0]
	value = info[2]
	opt = info[0][1]
	state = info[1] if 'state' not in opt else opt['state']
	mode = self.daw_vars['mode']
	if '--show-command' in main.queries:
		print(id,state,info,opt)

	## layouts toggles
	if id in range(921,925):
		modif('trig',id,state)
		
		if id in range(921,924):
			
			disp = id-920
			if state:
				# Entering alternative pages
				if disp in self.layouts['all'] or disp in self.layouts[daw.short_name]:
					speak("layout "+str(disp))
					self.layout_prepare(disp)
										
			else:
				# Leaving alternative pages
				self.layout_prepare(0)
				
	command_id = self.matrix['commands'][id] if id in self.matrix['commands'] else False
	button_type = 'user' if id not in self.matrix['plugin_buttons'][0] else 'plugin_button'
	pos = id if button_type == 'user' else self.matrix['plugin_buttons'][0][id]

	if state and modif('test',[910,911]) and id not in self.getting_in_exclude:
		if main.safety_check('question_access'):
			def to_thread():
				self.buttons.edit(button_type=button_type, pos=pos, disp=self.layout_active)
			Thread(target=to_thread).start()
			
	elif state and modif('test',[909,911]) and id not in self.getting_in_exclude:
		self.buttons.delete(button_type=button_type, pos=pos, disp=self.layout_active)
	else:
		if command_id:

			if isinstance(command_id,list):
				options = command_id[1]
				command_common(daw,self,command_id[0],info,options)
			
			if isinstance(command_id,dict):
				self.buttons.exec(button_type=button_type, pos=pos, velocity=info[2], state=info[1])