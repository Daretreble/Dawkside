from mido import Message as MidiMsg
from threading import Thread
import time

from classes.midisurfaces import MidiSurfaces
from .functions import *

class Keys:
	def __init__(self,main,data):
		self.act = False
		self.main = main
		self.control_assoc = False
		self.routing_destination = False
		self.velo_curve = False
		self.keys_init = False
		self.pre_midi = False
		self.__dict__.update(data)
		if 'control_assoc' in data['settings'] and data['settings']['control_assoc'] in main.devices['control']:
			self.control_assoc = main.devices['control'][data['settings']['control_assoc']]
		self.port = MidiSurfaces(self.ports,self.main,self.ports[2])
		if self.port.inport:
			Thread(target=self.midi_loop).start()
			if self.keys_init:
				self.keys_init[0](self)
			self.act = True
			self.notes_on = []
			self.zones_config = [
				[True,0,127,0,0,True],
			]
			self.zones_previous = self.zones_config
			self.zone_presets = [
				[
					[[True,0,127,0,0,True]],
					"Zone resetted to full range"
				],
				[
					[
						[True,0,54,0,0,True],
						[True,55,127,0,1,True],
					],
					"Orchestral split"
				]
			]
			print("Keys",self.name)
		else:
			print("Keys (Unavailable)",self.name)

	def panic(self):

		if self.routing_destination:
			for n in range(128):
				self.routing_destination.midiout(MidiMsg('note_off',note=n,channel=0,velocity=0))
			self.routing_destination.midiout(MidiMsg('control_change',control=120,channel=0,value=127))
			
Keys.zone_manage = zone_manage
Keys.midi_loop = midi_loop