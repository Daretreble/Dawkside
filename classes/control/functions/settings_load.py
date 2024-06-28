import json

def settings_load(self):
	""" Loads user settings. """

	with open(self.settings_path, 'r') as file:
		self.settings = json.load(file)