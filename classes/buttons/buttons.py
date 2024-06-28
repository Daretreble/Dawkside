from .functions import *

class Buttons:
	""" Manages control buttons. """
	
	def __init__(self,control):
		self.control = control

Buttons.delete = delete
Buttons.edit = edit
Buttons.exec = exec
Buttons.refresh = refresh