import os
import json
from functions.speak import speak

def param_save(self):
	""" Saves plugins pages. """
	plugins = self.plugins
	main = plugins.main

	if self.is_saved('plugin'):
		with open(f"plugins/settings/{plugins.name}.json", 'w') as file:
			json.dump(plugins.user_params[plugins.name], file,indent=1)
	else:
		speak('Nothing to save')
