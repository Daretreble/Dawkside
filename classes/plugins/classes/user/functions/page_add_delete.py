from functions.speak import speak

def page_add_delete(self,action):
	""" Adds and deletes pages. """
	plugins = self.plugins
	main = plugins.main
	modif = main.modif
		
	if plugins.page_type == 0:
	
		if modif('test',[911]):
		
			if action == 'add':
				speak("Adds a page before.")
			if action == 'delete':
				speak("Deletes the actual page.")
		
		else:
		
			if not self.is_saved('plugin'):
				self.page_create()
			
			if action == 'add':
				output1 = 'New page inserted, all subsequent pages are moved one position further'
				output2 = 'Create at least one page before inserting a new one'

				# Check if there's at least one page
				if plugins.user_params[plugins.name]:
					keys_to_modify = [key for key in plugins.user_params[plugins.name] if isinstance(key, int)]
					for key in sorted(keys_to_modify, reverse=True):
						if key >= plugins.page[0]:
							plugins.user_params[plugins.name][key + 1] = plugins.user_params[plugins.name][key]
							del plugins.user_params[plugins.name][key]
				else:
					# Handle case when there are no pages, and a new page needs to be added
					plugins.user_params[plugins.name][1] = {}  # Assuming the first page starts at 1
			
			if action == 'delete':
				output1 = "Page deleted. All subsequent pages are moved one position. To clear a page, use the page clear shortcut."

				if self.is_saved('page'):
					del plugins.user_params[plugins.name][plugins.page[0]]

				keys_to_modify = [key for key in plugins.user_params[plugins.name] if isinstance(key, int)]
				for key in keys_to_modify:
					if key > plugins.page[0]:
						plugins.user_params[plugins.name][key - 1] = plugins.user_params[plugins.name][key]
						del plugins.user_params[plugins.name][key]		
			
			self.param_save()
			speak(output1)
			plugins.daw.pVar = ['fxreload']
	
	else:
	
		speak("Switch to custom pages mode to manage pages.")
