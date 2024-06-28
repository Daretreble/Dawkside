import os
import json
import time
import re
from threading import Thread
from functions.misc import normalized_from_min_max,keys_to_int
from functions.speak import speak

def devices_manage(self,*args,**kwargs):

	main = self.main
	plugins = self.plugins
	action = kwargs['action']
	plugins = self.plugins
	
	def page_change():

		self.datatmp['osc_tracking']['page_load'][0] = True
		
		for _ in self.datatmp['listens']['parameters']:
			self.client.send_message('/live/device/stop_listen/parameter/value',_)
		self.datatmp['listens']['parameters'] = []

		params_to_activate = []
		if plugins.page_type == 0:
			if plugins.page[0] in plugins.user_params[plugins.name]:
				pgtmp = plugins.user_params[plugins.name][plugins.page[0]]
				if plugins.page[0] in plugins.user_params[plugins.name]:
					data = pgtmp['data']
					for key,value in data.items():
						params_to_activate.append(value['prm']-1)
		
		if plugins.page_type == 1:
			base = (plugins.page[0]-1)*8
			for _ in range(8):
				if (_+1)+base in plugins.params:
					params_to_activate.append(_+base)

		time.sleep(0.1)
		for _ in params_to_activate:
			tuple_tmp = [self.track.index[0],self.plugins.index[0]-1,_]
			self.client.send_message('/live/device/start_listen/parameter/value',tuple_tmp)
			self.datatmp['listens']['parameters'].append(tuple_tmp)

		time.sleep(0.1)
		plugins.user.manage()
		plugins.user.refresh(action='full')
		self.datatmp['osc_tracking']['page_load'][0] = False
	
	if action == 'page_change':
		page_change()
	
	if action == 'get_devices':

		self.switchtime = time.time()
	
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

			self.client.send_message('/live/device/get/parameters/name',(self.track.index[0],plugins.index[0]-1))
		else:
			plugins.act = False
			
	if action == 'get_parameter_names':

		plugins.params = {}

		count = 1
		for params in args[3:]:
			plugins.params[count] = {'prm':count,'name':params,'val':False,'valstr':False,'defval':False,'min':False,'max':False}
			count += 1
		plugins.param_count = len(plugins.params)
		self.client.send_message('/live/device/get/parameters/min',(self.track.index[0],plugins.index[0]-1))

	if action == 'get_parameter_values':
		
		count = 1
		for values in args[3:]:
			plugins.params[count]['valstr'] = values
			plugins.params[count]['defval'] = values
			count += 1
		self.client.send_message('/live/device/get/parameters/min',(self.track.index[0],plugins.index[0]-1))

	if action == 'get_parameter_mins':
		count = 1
		for mins in args[3:]:
			if count in plugins.params:
				plugins.params[count]['min'] = mins
			count += 1
		self.client.send_message('/live/device/get/parameters/max',(self.track.index[0],plugins.index[0]-1))

	if action == 'get_parameter_maxs':
		count = 1
		for maxs in args[3:]:
			if count in plugins.params:
				plugins.params[count]['max'] = maxs
				plugins.params[count]['val'] = normalized_from_min_max(plugins.params[count]['valstr'],plugins.params[count]['min'],maxs)
			count += 1	
		
		page_change()