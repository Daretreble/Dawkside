import mido

inport = mido.open_input("reaper_out 4")
outport = mido.open_output("reaper_in 4")

for msg in inport:
	if msg.type == 'sysex':
		output = ''
		for _ in msg.data:
			output += chr(_)
		print(output)
	outport.send(msg)