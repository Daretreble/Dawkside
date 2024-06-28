# Tracks class

class Tracks:
	def __init__(self,daw):
	
		self.daw = daw
		self.tracks = {}
		self.num = [0,0]
		self.index  = [0,0]
		daw.fre['tracks'] = {'volume':{},'pan':{}}
		for vp in ['volume','pan']:
			for _ in range(8):
				daw.fre['tracks'][vp][_] = {
					'pitch':[0.0,0.0],
					'name':vp,
					'valstr':None,
					}
					
	def setarm(self,track):
	
		for _ in range(8):
			state = 1 if _+self.offset == track else 0
			self.daw.client.send_message('/live/track/set/arm',(_+self.offset,state))