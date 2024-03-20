from functions.osc_setup import *
from classes.midisurfaces import MidiSurfaces
from threading import Thread

def startup(self):
	osc_set_client(self,'127.0.0.1',11000)
	osc_set_server(self,'127.0.0.1',11001)
	self.routing = MidiSurfaces(['live_out','live_in'],self.main,'startswith')
	self.client.send_message('/live/view/get/selected_track',True)

	Thread(target=self.process_loop).start()