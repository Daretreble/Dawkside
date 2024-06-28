import mido

inport = mido.open_input("routing_in 12")
outport = mido.open_output("3- POCKET-GT 17")

for msg in inport:
	print(msg)
	outport.send(msg)