# Plugins class

import time

from .functions import *
from .classes.user.user import User

class Plugins:
	""" Manage the selected plugin data and behavior """
	def __init__(self,daw):
		self.main = daw.main
		self.daw = daw
		self.user = User(self)
		self.user_params = {}
		self.act = False
		self.plugins_list = []
		self.index = [1,1]
		self.nfxs = 0
		daw.fre['plugins'] = {'faders':{},'ids':{},'btns':{'pos':[],'prm':{}}}
		self.switchtime = time.time()
		self.oscmatrix = {}
		self.preset = [False,'']
		self.name = ''
		self.fullname = ''
		self.subname = ''
		self.lastplugin = ''
		self.page = [1,'',1]
		self.page_type = 1
		self.param_count = 0
		self.paramsbank = 1
		self.last_touched = {
			'act':False,
			'name':'',
			'num':0,
			'val':0,
			'valstr':'',
			}
		self.rowhi = [0,[]]
		self.last_param = {'act':False}
		self.params = {}

Plugins.param_nav = param_nav
Plugins.plugin_nav = plugin_nav
Plugins.page_nav = page_nav
Plugins.type_select = type_select