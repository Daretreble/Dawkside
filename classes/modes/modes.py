from mido import Message as MidiMsg
from .classes import *
from functions.misc import model_rotary_menus
from common.scales import scales
from functions.speak import speak

class Modes:
	""" Manages playing modes. """
	def __init__(self,control):

		self.control = control
		self.main = self.control.main
		self.sections = {
			130:{'name':"Drum rack",'class':Drum_rack(self),'desc':"The Drum Rack control modes metamorphose your controller into an adaptable drum interface with customizable pads and additional features."},
			131:{'name':"Scaled pads",'class':Scaled_pads(self),'desc':"The scaled pad control mode empowers you to utilize your controller as a piano keyboard, complete with scale capabilities and tuning options."},
		}

	# Refreshes lights
	def refresh(self):

		mode = self.control.daw_vars['mode']
		for s in self.sections:
			c = 'mmdon' if s == self.control.daw_vars['mode'] else 'mmddim' if s < 130+len(self.sections) else 'off'
			self.control.matrix_in(s+300,c,action='unit')
	
	# All notes off
	def panic(self):
		for _ in range(128):
			self.control.daw.routing.midiout(MidiMsg('note_off',note=_,channel=0,velocity=0))
	
	def scales_nav(self,dir,action):
		dest = self.sections[self.control.daw_vars['mode']]['class']

		if action == 'nav':
			if dest.selected_scale + dir in range(len(scales)):
				dest.selected_scale += dir
				speak(scales[dest.selected_scale]['title'])
			dest.refresh()
	
	def transpose(self,id,info,action):
		dest = self.sections[self.control.daw_vars['mode']]['class']
		if action == 'reset':

			if id in[864,865]:
				dest.transpose_fine = 0
				speak("Fine transposition resetted")

			if id in[866,867]:
				dest.transpose_bank = 0
				speak("bank transposition resetted")
		
		if action == 'transpose':
		
			# Transpose fine
			if id in[864,865]:
				dir = -1 if id == 864 else 1
				dest.transpose_fine+=dir
				speak(f"{dest.transpose_fine} Fine")

			# Transpose bank
			if id in[866,867]:
				dir = -1 if id == 866 else 1
				dest.transpose_bank+=dir
				speak(f"Octave {dest.transpose_bank}")

		self.panic()
		dest.refresh()