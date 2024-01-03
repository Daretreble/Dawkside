import time
import os
import pprint
from mido import Message as MidiMsg
from common.scales import scales
from functions.speak import speak

class Scaled_pads:
	""" Manages Scales pads. """
	def __init__(self,modes):
		self.modes = modes
		self.control = self.modes.control
		self.main = self.control.main
		self.pads_position = {}
		self.bank_middle = 3
		self.transpose_bank = 0
		self.transpose_fine = 0
		self.fixed_velocity = 64
		self.pads_type = 1
		self.selected_scale = 0
		self.selected_root = 0

	def midi_in(self,state,note):
		if note in self.pads_feed:
			for f in self.pads_feed[note]:
				c = 'modes_sp_on' if state else self.scale_reference[f][1]
				self.control.matrix_in(f+800,c,action='unit')
	
	def pads_type_select(self):
		pass
	
	def refresh(self):

		self.scale_reference = {}
		self.pads_feed = {}
		degrees = scales[self.selected_scale]['act']
		ribbon = []

		# All scaled pads
		if self.pads_type == 1:
		
			o = 0
			for cycles in range(11):
				for degree in degrees:
					note = degree + (o*12)
					if note < 128:
						ribbon.append([note,degree])
				o += 1

			base = (len(degrees)*(self.bank_middle+self.transpose_bank))
			key = base
			for row in range(8):
				for col in range(8):
					pos = col + (row*8)
					note = ribbon[key][0]
					c = 'modes_sp_root' if ribbon[key][1] == 0 else 'modes_sp_scale'
					self.scale_reference[pos] = [note,c]
					if note in self.pads_feed:
						if pos not in self.pads_feed[note]:
							self.pads_feed[note].append(pos)
					else:
						self.pads_feed[note] = [pos]
					self.control.matrix_in(pos+800,c,action='unit')
					key += 1
				key -= 5

		# All notes, including off scale
		if self.pads_type == 2:
		
			o = 0
			for cycles in range(11):
				for degree in range(12):
					note = degree + (o*12)
					if note < 128:
						ref = False if degree not in degrees else degree
						ribbon.append([note,ref])
				o += 1

			base = (self.bank_middle*12)+(12*self.transpose_bank)
			key = base
			for row in range(8):
				for col in range(8):
					pos = col + (row*8)
					note = ribbon[key][0]
					c = 'modes_sp_dim' if ribbon[key][1] is False else 'modes_sp_scale' if ribbon[key][1] != 0 else 'modes_sp_root'
					self.scale_reference[pos] = [note,c]
					if note in self.pads_feed:
						if pos not in self.pads_feed[note]:
							self.pads_feed[note].append(pos)
					else:
						self.pads_feed[note] = [pos]
					self.control.matrix_in(pos+800,c,action='unit')
					key += 1
				key -= 3

	def trig(self,id,info):

		id-=800
		state = info[1]
		velo = info[2]
		
		note = self.scale_reference[id][0]

		if note in range(128):
			self.control.daw.routing.midiout(MidiMsg('note_on' if state else 'note_off',note=note,channel=0,velocity=velo))
			self.midi_in(state,note)
			
		elif state:
			speak("Out of range")