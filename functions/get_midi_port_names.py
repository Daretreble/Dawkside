import mido

def get_midi_port_names(ports):
	
	input_port = False
	output_port = False
	
	# Get input ports
	for pn in mido.get_input_names():
		if pn.startswith(ports[0]):
			input = pn

	# Get output ports
	for pn in mido.get_output_names():
		if pn.startswith(ports[1]):
			output = pn

	return [input,output]