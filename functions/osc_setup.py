from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from threading import Thread

def osc_set_client(self,ip,port):
	self.client = udp_client.SimpleUDPClient(ip,port)

def osc_set_server(self,ip,port):
	self.dispatcher = dispatcher.Dispatcher()
	self.dispatcher.map("*",self.osc)
	self.server = osc_server.ThreadingOSCUDPServer((ip,port), self.dispatcher)
	Thread(target=self.server.serve_forever).start()

