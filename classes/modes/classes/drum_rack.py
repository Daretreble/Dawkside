from mido import Message as MidiMsg
from functions.speak import speak

class Drum_rack:
	""" Manages Drum rack. """
	def __init__(self,modes):
		self.modes = modes
		self.control = self.modes.control
		self.main = self.control.main
		# bank size and bank 0 base note
		self.bank_size = [16,36]
		self.pads_position = {}
		self.pads_feed = {}
		self.transpose_bank = 0
		self.transpose_fine = 0
		self.fixed_velocity = 64

	def midi_in(self,state,note):
		if note in self.pads_feed:
			for f in self.pads_feed[note]:
				c = 'modes_dr_on' if state else 'modes_dr_regular'
				self.control.matrix_in(f+800,c,action='unit')
	
	def refresh(self):
		pads_on = []
		note = (self.transpose_bank * self.bank_size[0]) + self.transpose_fine + self.bank_size[1]
		for i in range(0,25,8):
			for j in range(4):
				pos = i+j
				self.pads_position.update({pos:note})
				if note in self.pads_feed:
					if pos not in self.pads_feed[note]:
						self.pads_feed[note].append(pos)
				else:
					self.pads_feed[note] = [pos]
				note+=1
				c = 'modes_dr_regular' if note-1 in range(128) else 'off'
				pads_on.append(pos)
				self.modes.control.matrix_in(pos+800,c,action='unit')
		
		for _ in range(64):
			if _ not in pads_on:
				self.modes.control.matrix_in(_+800,'off',action='unit')

	def trig(self,id,info):

		id-=800
		state = info[1]
		velo = info[2]
		
		if id in self.pads_position:

			note = self.pads_position[id]
			
			if note in range(128):
				self.control.daw.routing.midiout(MidiMsg('note_on' if state else 'note_off',note=note,channel=0,velocity=velo))
				self.midi_in(state,note)
			elif state:
				speak("Out of range")