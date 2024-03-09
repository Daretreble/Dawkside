import mido
import mido.backends.rtmidi

class MidiSurfaces:
	""" Manage midi control surfaces """
	def __init__(self,ports,main,searching):
		
		# Basic info
		self.ports = ports
		self.searching = searching
		self.inport = False
		self.outport = False
		
		# Get input port
		if self.ports[0]:
			for pl in mido.get_input_names():
				if self.searching == 'startswith':
					tested = pl.startswith(self.ports[0])
				if self.searching == 'contains':
					tested = self.ports[0] in pl
				if tested:
					try:
						self.inport = mido.open_input(pl)
						main.midi_ports.append(self.inport)
						self.inport.info = self.ports[0]
					except _rtmidi.SystemError as a:
						print(e)
		else:
			self.inport = False
		
		# Get output port
		if self.ports[1]:
			for pl in mido.get_output_names():
				if pl.startswith(self.ports[1]):
					self.outport = mido.open_output(pl)
					main.midi_ports.append(self.outport)
					self.outport.info = self.ports[0]
		else:
			self.outport = False
			
					
	def midiout(self,msg):
		if self.outport:
			self.outport.send(msg)