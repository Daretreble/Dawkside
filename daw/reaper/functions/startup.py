import time
import socket
from threading import Thread
from functions.osc_setup import *
from classes.midisurfaces import MidiSurfaces

def startup(self):

	self.routing = MidiSurfaces(['reaper_out','reaper_in'],self.main,'startswith')
	Thread(target=self.midi_loop).start()					

	def reaper_run():

		Thread(target=self.status_loop).start()
		osc_set_client(self,socket.gethostbyname(socket.gethostname()),8000)
		osc_set_server(self,'127.0.0.1',9000)

		def refresh_devices():
			time.sleep(1)
			self.client.send_message('/action',41743)
		Thread(target=refresh_devices).start()
	
	if self.reapy_mode:
		def reapy_test():
			try:
				import reapy
				from reapy import reascript_api as rpr
				self.reapy = reapy
				self.rpr = rpr
				reaper_run()
			except:
				time.sleep(1)
				reapy_test()
		reapy_test()
	else:
		reaper_run()