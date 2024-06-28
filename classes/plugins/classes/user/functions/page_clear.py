def page_clear(self,reload=True):

	plugins = self.plugins
	main = plugins.main
	
	del(plugins.user_params[plugins.name][plugins.page[0]])
	self.param_save()
	if reload:
		plugins.daw.pVar = ['trackreload']