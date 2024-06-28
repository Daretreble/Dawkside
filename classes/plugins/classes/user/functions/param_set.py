from functions.speak import speak

def param_set(self,dest,action):
	""" Sets the selected parameter on destination. """

	plugins = self.plugins
	daw = plugins.daw
	main = plugins.main
	
	if plugins.act:
	
		passed = True
	
		if action == 'delete':
		
			if self.is_saved('page') and dest in plugins.user_params[plugins.name][plugins.page[0]]['data']:
			
				tmp = plugins.user_params[plugins.name][plugins.page[0]]['data']
				output = plugins.params[tmp[dest]['prm']]['name']
				if dest in tmp:
					del tmp[dest]
					self.param_save()
					param_count = len(tmp)
					if len(tmp) == 0:
						speak("That page is now empty.")
					else:
						speak(f"{output} removed from fader {dest+1} in {plugins.page[1]} using {plugins.fullname}. {param_count} parameter{'s' if param_count >= 1 else ''} left in {plugins.page[1]}.")
						
			else:
				
				speak("Already empty.")
				passed = False
		
		if action == 'add':
		
			if plugins.last_param['act']:
		
				self.page_create()
				
				paramtmp = plugins.params[plugins.last_param['num']]
				plugins.user_params[plugins.name][plugins.page[0]]['data'][dest] = {
					'type':'prm',
					'prm':plugins.last_param['num'],
					'name':paramtmp['name'],
					'defval':round(paramtmp['defval'],4),
				}
				self.param_save()
				speak(f"{paramtmp['name']} added to fader {dest+1} in {plugins.page[1]} using {plugins.fullname}. Press Delete while pressing that fader to remove the parameter.")
			else:
				passed = False
				speak("Please select a parameter.")
		if passed:
		
			if daw.short_name == 'reaper':
				daw.pVar = ['fxreload']
			
			if daw.short_name == 'live':
				daw.client.send_message('/live/track/get/devices/name',(daw.track.index[0],0))
			
	else:
	
		speak("Please add a plugin.")