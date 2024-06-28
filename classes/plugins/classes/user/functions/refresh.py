def refresh(self,*args,**kwargs):
	""" Refreshes control matrix. """

	daw = self.plugins.daw
	plugins = self.plugins
	main = plugins.main
	action = kwargs['action']

	if action == 'unit':
		controls = [args[0]]

	if action == 'full':
		controls = daw.online['control']
			
	# Faders
	for m in controls:
		m.last_touched[0] = False
		self.rotarygroup_sel(m,action='refresh',speak=False)
			
	# Plugin user page buttons
	btns = False
	if self.is_saved('page') and len(plugins.user_params[plugins.name][plugins.page[0]]['plugin_button']) > 0:
		btns = plugins.user_params[plugins.name][plugins.page[0]]['plugin_button']
		
	for m in controls:
		m.layout_prepare(m.layout_active)
	
	# Plugins Page nav
	for _ in[376,377]:
		if _ == 376:
			c = 'dim1' if not plugins.act else 'plugins_pagenav_on' if plugins.page[0] > 1 else 'plugins_pagenav_off'
			for m in daw.online['control']:
				m.matrix_in(376,c,action='unit')
		if _ == 377:
			c = 'dim1' if not plugins.act else 'plugins_pagenav_on'
			for m in daw.online['control']:
				m.matrix_in(377,c,action='unit')

	# Plugins Plugin nav
	for _ in[378,379]:
		if _ == 378:
			c = 'dim1' if not plugins.act else 'plugins_plugnav_on' if plugins.index[0] > 1 else 'plugins_plugnav_offf'
			for m in daw.online['control']:
				m.matrix_in(378,c,action='unit')
		if _ == 379:
			c = 'dim1' if not plugins.act else 'plugins_plugnav_on' if plugins.index[0] < plugins.nfxs else 'plugins_plugnav_off'
			for m in daw.online['control']:
				m.matrix_in(379,c,action='unit')
	
	# Plugins page type refresh
	for _ in[380,381]:
		c_tmp = 'user' if _==380 else '8banks'
		c = 'dim1' if not plugins.act else 'plugins_pt_'+c_tmp+'_on' if plugins.page_type == _-380 else 'plugins_pt_'+c_tmp+'_off'
		for m in daw.online['control']:
			m.matrix_in(_,c,action='unit')
	
	# Plugin selection btns
	for _ in range(16):
		if plugins.act:
			c = 'plugins_plugsel_on' if _ == plugins.index[0]-1 else 'plugins_plugsel_off' if _ < plugins.nfxs else 'dim1'
		else:
			c = 'dim1'
		for m in daw.online['control']:
			m.matrix_in(_+360,c,action='unit')