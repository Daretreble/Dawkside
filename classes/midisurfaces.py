import mido
import mido.backends.rtmidi

class MidiSurfaces:
	""" Manage midi control surfaces """
	def __init__(self,ports,main):
		
		# Basic info
		self.ports = ports
		self.inport = False
		self.outport = False
		
		# Get input port
		if self.ports[0]:
			for pl in mido.get_input_names():
				if pl.startswith(self.ports[0]):
					self.inport = mido.open_input(pl)
					main.midi_ports.append(self.inport)
					self.inport.info = self.ports[0]
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