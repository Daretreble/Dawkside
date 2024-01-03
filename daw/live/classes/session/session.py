from .functions import *

class Session:
	""" Live's Session View manamgenent. """
	def __init__(self,daw):
		self.daw = daw
		
Session.refresh = refresh
Session.scroll = scroll
Session.slot_status = slot_status