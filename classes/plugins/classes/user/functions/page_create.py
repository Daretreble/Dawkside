def page_create(self):

	plugins = self.plugins
	main = plugins.main
	
	if not self.is_saved('plugin'):
		plugins.user_params[plugins.name] = {'zones':{}}
	if not self.is_saved('page'):
		plugins.user_params[plugins.name][plugins.page[0]] = {'page_name':'','data':{},'plugin_button':{}}