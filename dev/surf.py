from pyfirmata import Arduino, util
import time
import socket
from pythonosc import udp_client
import mido

# Use a fixed IP address for the OSC client
OSC_IP = '192.168.1.100'
OSC_PORT = 8000
client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

# Detect MIDI port
midi_port = None
for port_name in mido.get_output_names():
	if port_name.startswith('reaper_in'):
		midi_port = mido.open_output(port_name)
		break

# Initialize Arduino
board = Arduino('COM3')
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()

# Main loop
try:
	while True:
		value_tmp = board.analog[0].read()
		if value_tmp:
			final_value = int(value_tmp * 16383 - 8192)
			if midi_port:
				midi_port.send(mido.Message("pitchwheel", channel=0, pitch=final_value))
				prev_value = final_value
		time.sleep(0.01)

# Handle keyboard interrupt to gracefully exit the loop
except KeyboardInterrupt:
	pass

# Close resources
if midi_port:
	midi_port.close()
board.exit()
