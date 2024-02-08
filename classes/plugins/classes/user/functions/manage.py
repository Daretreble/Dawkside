import math
import os
import pprint
from functions.misc import pitch_convert

def manage(self):

	plugins = self.plugins
	main = plugins.main
	daw = plugins.daw
	
	plugins.last_touched['act'] = False
	daw.fre['plugins'] = {'faders':{},'ids':{},'btns':{}}
	ids = []
	
	try:
		if (self.plugins.page_type == 0 and self.is_saved('page')) or plugins.page_type == 1:
		
			## BANKS
			
			if plugins.page_type == 1:
			
				base = (plugins.page[0]-1)*8
				for _ in range(8):
				
					if (_+1)+base in plugins.params:
					
						if daw.short_name == 'reaper':
							
							if daw.reapy_mode:
								param = daw.track.reapy_track.fxs[plugins.index[0]-1].params[_+base]
								name = param.name
								value = param
								value_string = param.formatted
								min = False
								max = False
							else:
								param = plugins.params[_+base+1]
								name = param['name']
								value = param['val'] if 'val' in param else False
								value_string = param['valstr']
								min = False
								max = False
						
						if daw.short_name == 'live':
							param = plugins.params[_+base+1]
							name = param['name']
							value = param['val']
							value_string = param['valstr']
							min = param['min']
							max = param['max']
						
						paramtmp = plugins.params[(_+1)+base]
					
						daw.fre['plugins']['faders'][_] = {
							'name':name,
							'prm':(_+1)+base,
							'pitch':[round(value,4),round(value,4)],
							'min':min,
							'max':max,
						}
						
						if daw.short_name == 'reaper':
							plugins.params[(_+1)+base].update({
								'name':name,
								'prm':(_+1)+base,
								'val':round(value,4),
								'valstr':value_string,
							})
						
						daw.fre['plugins']['ids'][paramtmp['prm']] = [_]					
													
			
			## USER
			if plugins.page_type == 0:
			
				pgtmp = plugins.user_params[plugins.name][plugins.page[0]]

				if len(pgtmp['data']) == 0 and len(pgtmp['plugin_button']) == 0:
					
					self.page_clear(reload=False)
				
				else:
				
					if plugins.page[0] in plugins.user_params[plugins.name]:
						plugins.page[1] = plugins.user_params[plugins.name][plugins.page[0]]['page_name']
					else:
						plugins.page[1] = 'Empty page '+str(plugins.page[0])
					data = pgtmp['data']
					
					paramslist = []
					
					# DEV
					btns_tmp = {}
					for key,value in plugins.user_params[plugins.name][plugins.page[0]]['plugin_button'].items():
						if 'pressed' in value:
							for seq in value['pressed']:
								if seq['event_type'] == 'plugin_param':
									to_add = [float(seq['value']),False]
									if seq['param_id'] not in btns_tmp:
										btns_tmp[seq['param_id']] = {key:to_add}
									else:
										btns_tmp[seq['param_id']].update({key:to_add})
					
					daw.fre['plugins']['btns'] = btns_tmp
					"""plugin = plugins.user_params[plugins.name][plugins.page[0]]['plugin_button']
					if len(plugin) > 0:
						for key,value in plugin.items():
							if 'param_id' in value[0]['in']:
								prmtmp = value[0]['in']['param_id']
								if prmtmp <= plugins.param_count:
									daw.fre['plugins']['btns']['pos'].append(key)
									if prmtmp not in paramslist:
										paramslist.append(prmtmp)
									if value[0]['in']['param_id'] not in daw.fre['plugins']['btns']['prm']:
										daw.fre['plugins']['btns']['prm'][prmtmp] = [key]
									else:
										daw.fre['plugins']['btns']['prm'][prmtmp].append(key)"""
					
					for key,value in data.items():
						prmtmp = value['prm']
						if prmtmp not in paramslist:
							paramslist.append(prmtmp)
						
					paramslist.sort()
					
					for _ in paramslist:
						if _ <= plugins.param_count:
							param = daw.track.reapy_track.fxs[plugins.index[0]-1].params[_-1]
							plugins.params[_].update({
								'name':param.name,
								'prm':_,
								'val':round(param,4),
								'valstr':param.formatted,
							})
					
					for key,value in data.items():
						prmtmp = value['prm']
						if prmtmp <= plugins.param_count:
							param = plugins.params[prmtmp]
							row = (math.floor(key/8)+1)
							
							tmpname = param['name']
							
							daw.fre['plugins']['faders'][key] = {
									'name':tmpname,
									'prm':value['prm'],
								}
							daw.fre['plugins']['faders'][key].update({
								'pitch':[param['val'],param['val'],pitch_convert('v2p',param['val'])],
							})
							if value['prm'] not in daw.fre['plugins']['ids']:
								daw.fre['plugins']['ids'][value['prm']] = [key]
							else:
								daw.fre['plugins']['ids'][value['prm']].append(key)
	
	except KeyError:
		self.manage()