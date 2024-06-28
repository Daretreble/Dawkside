import time
import copy
import re
import os
import pprint
import json
from threading import Thread
from functions.misc import keys_to_int
from functions.speak import speak

def get_data(self,*args):
	""" Retrieves all startup data for Reaper."""
	
	main = self.main
	track = self.track
	plugins = self.plugins
	
	action = args[0]
	
	with self.reapy.inside_reaper():
	
		reapy_track = self.track.reapy_track
		
		if 'track' in args[0]:
			self.track.name = reapy_track.name
			self.track.index = [reapy_track.index,reapy_track.index]
			
			
			if reapy_track.id not in self.track.history:
				self.track.history.update({
					reapy_track.id:{
						'fx':False,'pg':False,'tr':{}}})
			hist = self.track.history[reapy_track.id]
			if hist['fx']:
				plugins.index = [hist['fx'],hist['fx']]
			if hist['pg']:
				plugins.user.page = [hist['pg'],'',hist['pg']]
			
			def zone_load(hist):
				if len(hist['tr']) > 0:
					for key,value in hist['tr'].items():
						if key in main.devices['keys']:
							#main.devices['keys'][key].panic()
							main.devices['keys'][key].zones_previous = main.devices['keys'][key].zones_config
							main.devices['keys'][key].zones_config = value
				else:
					for key,value in main.devices['keys'].items():
						#value.panic()
						value.zones_config = value.zones_previous
								
			self.client.send_message('/device/track/follows/last_touched',1.0)
			def delayed_refresh():
				time.sleep(0.1)
				self.track.refresh(action='full')
				self.switch_on = False
			Thread(target=delayed_refresh).start()					
			plugins.switchtime = time.time()
		
		if 'sendrecv' in args[0]:
		
			sends = reapy_track.sends
			self.track.nsend = len(sends)
			recvs = reapy_track.receives
			self.track.nrecv = len(recvs)
			self.fre['track']['send'] = {}
			self.fre['track']['recv'] = {}
			for _ in range(self.track.nsend):
				tmp = sends[_]
				self.fre['track']['send'].update({
					_:{
						'name':tmp.dest_track.name,
						'pitch':[0.0,0.0],
						'valstr':'',
						}
					})
			for _ in range(self.track.nrecv):
				tmp = recvs[_]
				self.fre['track']['recv'].update({
					_:{
						'name':tmp.source_track.name,
						'pitch':[0.0,0.0],
						'valstr':'',
						}
					})
					
			if 'track' not in args[0]:
				self.client.send_message('/device/track/follows/last_touched',1.0)
				#self.client.send_message('/action',41743)

		if 'fx' in args[0]:

			if reapy_track.n_fxs > 0:
				if 'plugins' in args[0]:
					plugins.plugins_list =  []
					for _ in reapy_track.fxs:
						plugins.plugins_list.append([_.name])
				plugins.act = True
				plugins.nfxs = len(plugins.plugins_list)
				if plugins.index[0] > plugins.nfxs:
					plugins.index[0] = 1
					if self.track.history[reapy_track.id]['pg'] == False:
						plugins.user.page = [1,'',1]
				pltmp = reapy_track.fxs[plugins.index[0]-1]
				plugins.param_count = pltmp.n_params
				pf = pltmp.name.split(':')[1].strip() if ': ' in pltmp.name else pltmp.name.strip()
				pf = pf.split('##')
				plugins.subname = pf[1] if len(pf) > 1 else ''
				plugins.fullname = "".join(re.split("\(|\)|\[|\]", pf[0])[::2])
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
				else:
					os.system('cls')
					speak("Building a data file for "+plugins.fullname+". Please wait about "+str(round(plugins.param_count/361))+" seconds. That is a one time operation for that plugin.",printout=True)
					paramsdata = {}
					with self.reapy.inside_reaper():
						for _ in range(plugins.param_count):
							tmp = reapy_track.fxs[plugins.index[0]-1].params[_]
							paramsdata.update({_+1:{
								'name':tmp.name,
								'defval':round(tmp,4),
								'valstr':'',
							}})
						with open(plugin_temp_path, 'w') as file:
							json.dump(paramsdata, file,indent=1)
						plugins.params.update(paramsdata)
						os.system('cls')
						speak("Done!",printout=True)
				if 'hist' in locals() and len(hist['tr']) == 0 and plugins.user.is_saved('plugin') and 'zones' in plugins.user_params[plugins.name] and plugins.subname in plugins.user_params[plugins.name]['zones']:
					for key,value in plugins.user_params[plugins.name]['zones'][plugins.subname].items():
						for k,v in main.devices['keys'].items():
							if k == key:
								self.track.history[self.track.reapy_track.id]['tr'][k] = copy.deepcopy(value)
								v.zones_config = value
								v.panic()
				else:
					if 'hist' in locals() and self.transpose_save:
						zone_load(hist)
				plugins.user.manage()
				self.client.send_message('/device/fx/select',plugins.index[0])
				self.client.send_message('/device/fxparam/count',pltmp.n_params)
			else:
				if 'hist' in locals() and self.transpose_save:
					zone_load(hist)
				plugins.act = False
				plugins.nfxs = 0
				plugins.plugins_list = []
				plugins.param_count = 0
				plugins.fullname = ''
				plugins.name = ''
			plugins.user.refresh(action='full')	
	
	main.play_sound('ready')