from .functions import *

class Track:
	""" Manage the selected track data and behavior """
	def __init__(self,daw):
		
		self.daw = daw
		self.name = ''
		self.history = {}
		self.index = [0,0]
		self.n_send = 0
		self.n_recv = 0
		self.send_recv_output = {'send':'Send','recv':'Receive'}
		daw.fre['track'] = {'track':{},'send':{},'recv':{}}
		daw.fre['track']['track'][6] = {
			'pitch':[0,0],
			'name':'Pan',
			'valstr':None,
			}
		daw.fre['track']['track'][7] = {
			'pitch':[0.0,0.0],
			'name':'Volume',
			'valstr':None,
			
			}
		
Track.refresh = refresh
Track.send_recv_select = send_recv_select