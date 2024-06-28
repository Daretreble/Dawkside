import os
import mido

for _ in mido.get_output_names():
	if _.startswith('MIDIOUT2 (Ableton Push)'):
		outport = mido.open_output(_)
for _ in mido.get_input_names():
	if _.startswith('MIDIIN2 (Ableton Push)'):
		inport = mido.open_input(_)
		

pos = 0

for _ in range(128):
	outport.send(mido.Message('note_on',channel=
	0,note=_,velocity=0))

for msg in inport:
	if msg.type == 'control_change':
		if msg.control == 14:
			dir = 1 if msg.value == 1 else -1
			pos+=dir
			if pos <= 0:
				pos = 0
			if pos >= 128:
				pos = 127
			os.system('cls')
			print(pos)
			outport.send(mido.Message('control_change',channel=
	0,control=86,value=pos))