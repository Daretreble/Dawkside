import time
import pprint
import os
from mido import Message as MidiMsg

def matrix_in(self,*args,**kwargs):
	
	action = kwargs['action']
	matrix = self.matrix
	daw = self.daw
	
	def trig(color,msg):
		output = self.colors[color if color in self.colors else 'on']
		tmp = False
		tosend = []
		if isinstance(output,list):
			if isinstance(output[0],list):
				tosend = output[0]
			else:
				tosend = [[output[0],output[1]]]
		else:
			tosend= [[output,0]]
			
		for _ in tosend:
			if msg[0]['model'] == 'nt':
				tmp = MidiMsg('note_on',channel=_[1],note=msg[1],velocity=_[0])
			if msg[0]['model'] == 'cc':
				tmp = MidiMsg('control_change',channel=_[1],control=msg[1],value=_[0])
			if msg[0]['model'] == 'sy':
				_[1][8] = msg[1]
				data = tuple(_[1])
				tmp = MidiMsg('sysex',data=data)
			if tmp:
				self.port.midiout(tmp)
			
	if action == 'commands':

		matrix['commands'].update({args[0]:args[1]})
		if isinstance(args[1],dict):
			for types in ['pressed','released']:
				if types in args[1]:
					for btn in args[1][types]:
						if btn['event_type'] == 'command':
							refer_id = btn['id']
							pos = args[0]
							if refer_id in matrix['refer']:
								if pos not in matrix['refer'][refer_id]:
									matrix['refer'][refer_id].append(pos)
							else:
								matrix['refer'].update({refer_id:[pos]})
							
		if isinstance(args[1],list):
			refer_id = args[1][0]
			pos = args[0]
			if refer_id in matrix['refer']:
				if pos not in matrix['refer'][refer_id]:
					matrix['refer'][refer_id].append(pos)
			else:
				matrix['refer'].update({refer_id:[pos]})
	
	if action == 'full' and self.getting_in:

		for key,value in self.getting_in.items():
			if key in matrix['commands']:
				button = matrix['commands'][key]
				if isinstance(button,list):
					if matrix['commands'][key][0] in self.refer_colors:
						c = self.refer_colors[matrix['commands'][key][0]]
						trig(c,self.getting_in[key])
				elif isinstance(button,dict):
					self.buttons.refresh(key,matrix['commands'][key])
			else:
				trig('off',self.getting_in[key])
	
	if action == 'unit':

		id = args[0]

		self.refer_colors.update({args[0]:args[1]})

		if self.getting_in and id in matrix['refer']:
			for refers in matrix['refer'][id]:
				if refers in self.getting_in:
					trig(args[1],self.getting_in[refers])
		elif 'direct' in kwargs:
			try:
				trig(args[1],self.getting_in[id])
			except KeyError:
				pass
