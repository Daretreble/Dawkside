import mido

inport = mido.open_input("ZOOM 1 Series 13")

for msg in inport:
	print(msg)