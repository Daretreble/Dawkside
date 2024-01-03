import os
import pprint
import json
import time
import re
from functions.misc import normalized_from_min_max,keys_to_int
from functions.speak import speak

def devices_manage(self,*args,**kwargs):

	main = self.main
	plugins = self.plugins
	action = kwargs['action']
	
	plugins = self.plugins
	
	if action == 'get_devices':
	
		plugins.plugins_list =  []
		for device in args[2:]:
			plugins.plugins_list.append([device])
		plugins.nfxs = len(plugins.plugins_list)
		plugins.act = False if plugins.nfxs == 0 else True

		if plugins.nfxs > 0:
			plugins.act = True
			if plugins.index[0] > plugins.nfxs:
				plugins.index[0] = 1
			plugin_tmp = plugins.plugins_list[plugins.index[0]-1][0]
			plugins.fullname = plugin_tmp
			plugins.name = plugins.fullname.replace(' ','').lower()
			plugins.name = re.sub('[\W_]+', '',plugins.name)
			if plugins.name not in plugins.user_params:
				plugin_settings_path = os.path.join('plugins','settings',self.short_name,plugins.name+'.json')
				if os.path.isfile(plugin_settings_path):
					with open(plugin_settings_path, 'r') as file:
						tmp_data = json.load(file)
						plugins.user_params[plugins.name] = keys_to_int(tmp_data)
				
				plugin_temp_path = os.path.join('plugins','temp',self.short_name,plugins.name+'.json')
				if os.path.isfile(plugin_temp_path):
					with open(plugin_temp_path, 'r') as file:
						tmp_data = json.load(file)
						plugins.params = keys_to_int(tmp_data)
						plugins.user.manage()
						plugins.user.refresh(action='full')
				else:
					self.client.send_message('/live/device/get/parameters/name',(self.track.index[0],plugins.index[0]-1))
		else:
			plugins.act = False
			
	if action == 'get_parameter_names':

		plugins.params_tmp = {}

		count = 1
		for params in args[3:]:
			plugins.params_tmp[count] = {'prm':count,'name':params,'val':False,'valstr':False,'defval':False,'min':False,'max':False}
			count += 1
		plugins.param_count = len(plugins.params_tmp)
		self.client.send_message('/live/device/get/parameters/value',(self.track.index[0],plugins.index[0]-1))

	if action == 'get_parameter_values':
		count = 1
		for values in args[3:]:
			plugins.params_tmp[count]['valstr'] = values
			count += 1
		self.client.send_message('/live/device/get/parameters/min',(self.track.index[0],plugins.index[0]-1))

	if action == 'get_parameter_mins':
		count = 1
		for mins in args[3:]:
			plugins.params_tmp[count]['min'] = mins
			count += 1
		self.client.send_message('/live/device/get/parameters/max',(self.track.index[0],plugins.index[0]-1))

	if action == 'get_parameter_maxs':
		count = 1
		for maxs in args[3:]:
			plugins.params_tmp[count]['max'] = maxs
			plugins.params_tmp[count]['val'] = normalized_from_min_max(plugins.params_tmp[count]['valstr'],plugins.params_tmp[count]['min'],maxs)
			count += 1	
		self.client.send_message('/live/device/get/parameters/default_value',(self.track.index[0],plugins.index[0]-1))
		
	if action == 'get_parameter_defaultss':
		count = 1
		for default_values in args[3:]:
			plugins.params_tmp[count]['defval'] = default_values
			count += 1

		os.system('cls')
		speak("Building a data file for "+plugins.fullname+". Please wait about "+str(round(plugins.param_count/361))+" seconds. That is a one time operation for that plugin.",printout=True)
		plugin_temp_path = os.path.join('plugins','temp',self.short_name,plugins.name+'.json')
		with open(plugin_temp_path, 'w') as file:
			json.dump(plugins.params_tmp, file,indent=1)
			plugins.params.update(plugins.params_tmp)
			os.system('cls')
			speak("Done!",printout=True)
			#plugins.params = plugins.params_tmp