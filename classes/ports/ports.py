from mido import Message as MidiMsg
from threading import Thread
import time

from classes.midisurfaces import MidiSurfaces
from .functions import *

class Ports:
	def __init__(self,main,data):
		self.act = False
		self.main = main
		self.control_assoc = False
		self.routing_destination = False
		self.ports_init = False
		self.pre_midi = False
		self.__dict__.update(data)
		self.port = MidiSurfaces(self.ports,self.main,self.ports[2])
		if self.port.inport:
			#Thread(target=self.midi_loop).start()
			if self.ports_init:
				self.ports_init[0](self)
			self.act = True
			print("Port",self.name)
		else:
			print("Port (Unavailable)",self.name)
			
Ports.midi_loop = midi_loop