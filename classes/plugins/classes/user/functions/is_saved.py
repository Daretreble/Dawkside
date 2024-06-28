def is_saved(self,spectrum):

	plugins = self.plugins
	main = plugins.main
	
	if spectrum == 'plugin':
		return True if plugins.name in plugins.user_params else False

	if spectrum == 'page':
		return True if plugins.name in plugins.user_params and plugins.page[0] in plugins.user_params[plugins.name] else False