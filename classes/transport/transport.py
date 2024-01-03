from functions.speak import speak

class Transport:
	""" Transport class. """
	def __init__(self,daw):
		self.daw = daw
		self.main = self.daw.main
		self.triggers = self.daw.triggers['transport']
		self.osc_triggers = {}
		for key,value in self.triggers.items():
			if value[1][0] not in self.osc_triggers:
				self.osc_triggers[value[1][0]] = [key]
			else:
				self.osc_triggers[value[1][0]].append(key)

	def status(self,id):
		if isinstance(id,int):
			return self.triggers[id][3]
		else:
			ids = []
			for key,value in self.triggers.items():
				if id == 'active':
					if value[3]:
						ids.append(key)
				if id == 'inactive':
					if not value[3]:
						ids.append(key)
			return ids

	def osc_manage(self,id,state):
		for id in self.osc_triggers[id]:
			transport = self.triggers[id]
			transport[3] = True if transport[1][1] == state else False
			if transport[4]:
				if isinstance(transport[4],list):
					output = transport[4][0] if transport[3] else transport[4][1]
				else:
					output = transport[4]
				speak(output)
			self.set(id)
	
	def help(self,id):
		transport = self.triggers[id]
		if isinstance(transport[5],list):
			output = transport[5][transport[3]]
		else:
			output = transport[5]
		speak(output)
	
	def set(self,id):
		transport = self.triggers[id]
		c = "tr_"+transport[0]+"_on" if transport[3] else "tr_"+transport[0]+'_off'
		for m in self.daw.online['control']:
			m.matrix_in(id,c,action='unit')

	def trig(self,id,params):
		transport = self.triggers[id]
		if isinstance(transport[2][0],list):
			to_send = transport[2][1] if transport[3] else transport[2][0]
		else:
			to_send = transport[2]
		self.daw.client.send_message(to_send[0],to_send[1])