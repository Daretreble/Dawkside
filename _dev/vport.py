import time
import mido
virtual_port_name = "Your Virtual MIDI Port Name"  # Replace with your desired port name
output_port = mido.open_output(virtual_port_name, virtual=True)

while True:
	print(output_port)
	time.sleep(3)