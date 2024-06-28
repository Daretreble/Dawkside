import os
import json
from functions.speak import speak

def param_save(self):
	""" Saves plugins pages. """
	
	plugins = self.plugins
	main = plugins.main

	if self.is_saved('plugin'):
		plugin_settings_path = os.path.join('plugins','settings',plugins.daw.short_name,plugins.name+'.json')
		with open(plugin_settings_path, 'w') as file:
			json.dump(plugins.user_params[plugins.name], file,indent=1)
	else:
		speak('Nothing to save')
