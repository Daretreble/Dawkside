import time
import os
import pprint
import json
from mido import Message as MidiMsg
from threading import Thread
from classes.buttons.buttons import Buttons
from classes.modes.modes import Modes
from classes.midisurfaces import MidiSurfaces
from functions.misc import keys_to_int
from functions.speak import speak
from .functions import *

class Control:
	""" Control surface management class. """
	def __init__(self,main,data):
		
		self.main = main
		self.modes = Modes(self)
		self.buttons = Buttons(self)
		self.switchtime = time.time()
		
		# defaults
		self.routing_destination = False
		self.fre_count = 8
		self.getting_in = False
		self.going_out = False
		self.colors = False,
		self.pre_midi = False
		self.post_midi = False
		self.faders_speak = [False,False]
		self.row_def = ['Faders','A','B','C']
		self.touch_tolerance = False
		self.toggle_type = False
		
		self.__dict__.update(data)
		self.getting_in_exclude = [240, 251, 252, 253] + list(range(200, 232))
		self.layout_active = 0
		self.fader_state = [[False, 0, 0, 0, time.time()] for _ in range(32)]
		self.last_touched = [False,time.time()]
		self.faders = {
			'track':{},
			'plugins':{},
			'midicc':{},
		}
		self.constants = {}
		"""
		for daws in main.daws:
			self.constants[daws.short_name] = {
				'refer_colors':{},
			}
		"""

		self.port = MidiSurfaces(self.ports,self.main,self.ports[2])
		if self.port.inport:
			for _ in range(128):
				if not self.toggle_type:
					self.port.midiout(MidiMsg('note_off',note=_,channel=0,velocity=0))
				else:
					if self.toggle_type == 1:
						self.port.midiout(MidiMsg('note_on',note=_,channel=0,velocity=0))
				self.port.midiout(MidiMsg('control_change',control=_,channel=0,value=0))
			
			# Load settings
			self.settings_path = os.path.join('devices','control',self.short_name,'settings.json')
			if os.path.isfile(self.settings_path):
				self.settings_load()
			else:
				self.default_settings = {
					'selected_daw':'reaper',
					'layout':'default',
				}
				self.settings_save(self.default_settings)
				self.settings = self.default_settings
			self.control_init[0](self)
			if '--use-default-layouts' in main.queries:
				self.layouts = self.default_layout
			else:
				layout_path = os.path.join('devices','control',self.short_name,'layouts',self.settings['layout']+'.json')
				if os.path.isfile(layout_path):
					with open(layout_path, 'r') as file:
						self.layouts = keys_to_int(json.load(file))
				else:
					self.layouts = self.default_layout
					self.settings['layout'] == 'default'
					self.layout_save()
			def delayed():
				if len(self.main.daws) == 0:
					time.sleep(1)
					delayed()
				else:
					time.sleep(1)
					self.daw_prepare()
				Thread(target=self.midi_loop).start()
			Thread(target=delayed).start()
			print("Control",self.name)
		else:
			print("Control (unavailable)",self.name)

	def daw_routing(self,**kwargs):

		speak_out = True if 'speak' in kwargs else False
		daw_tmp = self.daw
		if 'daw' in kwargs:
			self.daw = self.main.daws[kwargs['daw']]

		for key,value in self.main.devices['keys'].items():
			if value.control_assoc and self.main.devices['keys'][key].control_assoc.name == self.name:
				self.keys_assoc = self.main.devices['keys'][key]
				self.main.devices['keys'][key].routing_destination = daw_tmp.routing
				self.main.devices['keys'][key].panic()
		if speak_out:
			speak("Keys routed to "+daw_tmp.name)

Control.daw_prepare = daw_prepare
Control.layout_prepare = layout_prepare
Control.fre_action = fre_action
Control.fre_feedback = fre_feedback
Control.fre_process = fre_process
Control.layout_save = layout_save
Control.matrix_send = matrix_send
Control.matrix_in = matrix_in
Control.midi_in_dispatch = midi_in_dispatch
Control.midi_loop = midi_loop
Control.mode_select = mode_select
Control.settings_load = settings_load
Control.settings_save = settings_save