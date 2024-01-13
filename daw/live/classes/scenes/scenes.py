import time
from functions.speak import speak

class Scenes:
	""" Manages Live's scenes information. """
	def __init__(self,daw):
	
		self.daw = daw
		self.index = [0,0]
		
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