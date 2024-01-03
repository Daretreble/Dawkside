import os
import pprint
import time
import time
from functions.misc import merge_dicts

def layout_prepare(self,disp,**kwargs):
	""" Generates all buttons on the selected layout. """

	daw = self.daw
	plugins = daw.plugins
	main = daw.main
	mode = self.daw_vars['mode']
	self.layout_active = disp
	self.matrix = {'commands':{},'refer':{},'plugin_buttons':[{},{}] }

	if self.daw.short_name not in self.layouts:
		self.layouts['reaper'] = self.default_layout[self.daw.short_name] if self.daw.short_name in self.layouts else {}

	permanent_list = merge_dicts(
		self.layouts['all']['permanent'].copy() if 'permanent' in self.layouts['all'] else {},
		self.layouts[self.daw.short_name]['permanent'].copy() if 'permanent' in self.layouts[self.daw.short_name] else {}
	)
	layouts = merge_dicts(
		self.layouts['all'][disp].copy() if disp in self.layouts['all'] else {},
		self.layouts[self.daw.short_name][disp].copy() if disp in self.layouts[self.daw.short_name] else {}
	)
	common_list = layouts['common'] if 'common' in layouts else {}
	mode_exclusive_list = layouts[mode] if mode in layouts else {}
	final_list = merge_dicts(permanent_list,common_list,mode_exclusive_list)

	for key,value in final_list.items():
		if isinstance(value,list):
			if value[0] in range(260,292):
				self.matrix['plugin_buttons'][0][key] = value[0]-260
				
				if value[0]-260 not in self.matrix['plugin_buttons'][1]:
					self.matrix['plugin_buttons'][1][value[0]-260] = []
				if key not in self.matrix['plugin_buttons'][1][value[0]-260]:
					self.matrix['plugin_buttons'][1][value[0]-260].append(key)
				
				if daw.plugins.act and daw.plugins.page_type == 0 and daw.plugins.user.is_saved('page'):
					if value[0] - 260 in plugins.user_params[daw.plugins.name][daw.plugins.page[0]]['plugin_button']:
						btn = plugins.user_params[daw.plugins.name][daw.plugins.page[0]]['plugin_button'][value[0]-260]
						self.matrix_in(key,btn,action='commands')
			else:
				self.matrix_in(key,value,action='commands')
		if isinstance(value,dict):
			self.matrix_in(key,value,action='commands')
	self.matrix_in(action='full')