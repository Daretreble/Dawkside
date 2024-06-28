from functions.speak import speak

def param_nav(self,dir,**kwargs):
	""" Scrolls through plugin parameters. """
	main = self.main
	modif = main.modif

	action = kwargs['action']

	if self.act:

		data = self.params
		max_params = len(data)

		if action == 'nav':
		
			if not self.last_param['act']:
				pos = 0
			else:
				pos = self.last_param['num']
			
			if modif('test',[900]):
				pos = int(pos // 8) * 8
				pos += (dir*8)+1
			else:
				pos += dir
			if pos < 1:
				pos = 0
			if pos > 0:
				if pos > max_params:
					pos = max_params
				self.last_param = {'act':True,'num':pos}
				speak(str(pos-1)+" "+data[self.last_param['num']]['name'])
			else:
				self.last_param = {'act':False}
				speak('None selected')
	else:
		speak("Please add a plugin.",repeat=False)