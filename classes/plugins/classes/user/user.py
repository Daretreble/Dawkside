from .functions import *

class User:
	def __init__(self,plugins):
		self.plugins = plugins
		self.param_sel = 1
		
		
User.is_saved = is_saved
User.manage = manage
User.page_add_delete = page_add_delete
User.page_clear = page_clear
User.page_create = page_create
User.page_rename = page_rename
User.param_save = param_save
User.param_set = param_set
User.refresh = refresh
User.rotarygroup_sel = rotarygroup_sel