import mido

inport = False
for p in mido.get_input_names():
	if 'APC MINI' in p:
		inport = mido.open_input(p)

for p in mido.get_output_names():
	if 'POCKET-GT' in p:
		outport = mido.open_output(p)

for msg in inport:
	if msg.type == 'control_change' and msg.control == 48:
		msg.channel = 14
		msg.control = 3
		outport.send(msg)