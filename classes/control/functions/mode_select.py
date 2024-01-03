from functions.speak import speak

def mode_select(self,*args,**kwargs):
	""" Manages mode selection. """

	daw = self.daw
	main = daw.main

	type = kwargs['mode'][0]
	mode = kwargs['mode'][1]
	launch = [False,False]
	
	# Mode selection
	if type == 1:

		mode_type = daw.modes if mode in range(100,108) else self.modes.sections

		for key,value in mode_type.items():
			if mode == key:
				if 'assoc' in value:
					launch = [key,value['assoc']]
				else:
					launch = [key,self.daw_vars['outmode']]
		
	# Output mode selection
	if type == 2:

		mode_type = daw.modes if self.daw_vars['mode'] in range(100,108) else self.modes.sections
	
		launch = [False,mode]
		
	if launch[0]:
		self.daw_vars['mode'] = launch[0]
	if launch[1]:
		self.daw_vars['outmode'] = launch[1]
	self.settings_save(self.settings)
	self.layout_prepare(0)
	# Mode action
	if launch[0] != False:
	
		tmp = launch[0]

		if self.daw_vars['mode'] in range(100,108):
			for _ in range(100,108):
				c = 'daw_modes_on' if _ == self.daw_vars['mode'] else 'daw_modes_dim' if _ < 100+len(daw.modes) else 'daw_modes_off'
				self.matrix_in(_+300,c,action='unit')
		
		if self.daw_vars['mode'] in range(130,138):
			for _ in range(130,138):
				c = 'control_modes_on' if _ == self.daw_vars['mode'] else 'control_modes_dim' if _ < 130+len(self.modes.sections) else 'control_modes_off'
				self.matrix_in(_+300,c,action='unit')
		
		if tmp in range(100,108):
			daw.refresh(self,tmp)
		if tmp in range(130,138):
			self.modes.sections[self.daw_vars['mode']]['class'].refresh()
		
	# Output mode action
	if launch[1]:
	
		tmp = launch[1]
		self.daw_vars['outmode'] = tmp

		if launch[1] == 11:
			daw.track.refresh(self,action='unit')
		if launch[1] == 12:
			daw.plugins.user.refresh(self,action='unit')

		for _ in range(10,18):
			c = 'output_modes_on' if _ == self.daw_vars['outmode'] else 'output_modes_dim' if _ < 10+len(main.outmodes) else 'output_modes_off'
			self.matrix_in(_+400,c,action='unit')
		
	output = mode_type[self.daw_vars['mode']]['name']
	if launch[1] != False:
		output+=' using '+main.outmodes[self.daw_vars['outmode']]['name']
	if kwargs['speak']:
		speak(daw.name+" "+output)