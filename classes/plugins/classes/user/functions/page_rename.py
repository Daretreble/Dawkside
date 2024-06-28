import os
from functions.speak import speak

def page_rename(self):
	""" Renames plugins pages. """	
	plugins = self.plugins
	
	if plugins.page_type == 0:

		plugins = self.plugins
		main = plugins.main

		modif = main.modif
	
		if modif('test',[911]):
		
			speak("Rename the actual page.")
		
		else:
		
			if self.is_saved('page'):
				os.system('cls')
				confirmquest = f"Choose a new name for {plugins.page[1]} which is physically at position {plugins.page[0]} using {plugins.fullname} or 'exit' to cancel."
				speak(confirmquest)
				confirm = input(confirmquest+': ')
				if confirm != 'exit':
					self.page_create()
					plugins.user_params[plugins.name][plugins.page[0]]['page_name'] = confirm
					self.param_save()
					os.system('cls')
					speak(f"Page renamed to {confirm}",printout=True)
				else:
					os.system('cls')
					speak("Page renaming cancelled.")
			else:
				speak("No page yet. Add faders and buttons to that page before renaming it.")

	else:
		speak("Switch to custom pages mode to rename a page.")
