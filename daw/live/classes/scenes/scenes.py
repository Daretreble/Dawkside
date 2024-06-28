import time
from functions.speak import speak

class Scenes:
	""" Manages Live's scenes information. """
	def __init__(self,daw):
	
		self.daw = daw
		self.index = [0,0]
		self.num = [0,0]
		
	def select(self,*args,**kwargs):

		action = kwargs['action']
		
		if action == 'nav':
			
			dir = args[0]
			new_scene = self.index[0] + dir
			if new_scene in range(0,self.num[0]):
				speak(new_scene+1)
				self.daw.client.send_message('/live/view/set/selected_scene',new_scene)
	
	def trig(self,*args,**kwargs):
	
		action = kwargs['action']
		daw = self.daw
		main = daw.main
		
		tracks = daw.tracks
		
		selected_scene = args[0]
		
		if action == 'fire' and time.time()-daw.switchtime > 0.5:
			daw.switchtime = time.time()
			for key,value in tracks.tracks.items():
				if value['clips'][selected_scene]:
					daw.clips.trig(key,selected_scene,action='fire')
				else:
					if value['stop_button'][selected_scene]:
						daw.client.send_message('/live/clip_slot/stop',(key,value['playing']))
			speak(selected_scene+1)