def daw_prepare(self):
	""" Prepares the control surface for the selected daw. """
		
	main = self.main
	
	if self.settings['selected_daw'] in main.daws:
		self.daw = main.daws[self.settings['selected_daw']]
	else:
		self.daw = main.daws[main.daws_index[0]]
	self.daw.online['control'].append(self)
	if self.daw.short_name not in self.settings:
		self.settings[self.daw.short_name] = {
			'mode':101,
			'outmode':11,
			'sendrecv':{
				'selected':'send',
			},
			'rotary_group':1,
			'mode_type':1,
		}
	if hasattr(self.daw,'exclusive'):
		self.settings[self.daw.short_name].update(self.daw.exclusive)
	self.daw_vars = self.settings[self.daw.short_name]
	self.refer_colors = {}
	
	self.matrix = {
		'commands':{},
		'refer':{},
		'user_refer':{},
	 	'plugin_refer':{},
	}

	self.mode_select(mode=[1,self.daw_vars['mode']],speak=True)
	self.daw_routing()