import json

def settings_save(self,to_save):
	""" Saves user settings. """

	with open(self.settings_path, 'w') as file:
		json.dump(to_save, file,indent=1)