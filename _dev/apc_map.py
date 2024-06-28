import os
import mido
from threading import Thread

inports = mido.get_input_names()
outports = mido.get_output_names()

for _ in inports:
	if 'APC MINI' in _:
		apc_in = mido.open_input(_)
	if 'live_bridge_out' in _:
		live_in = mido.open_input(_)

for _ in outports:
	if 'APC MINI' in _:
		apc_out = mido.open_output(_)
	if 'live_bridge_in' in _:
		live_out = mido.open_output(_)

def apc_loop_in():
	for msg in apc_in:
		if msg.type == 'note_on' and msg.note == 98:
			os.system('cls')
			#print('apc in',msg)
		live_out.send(msg)
Thread(target=apc_loop_in).start()

def live_loop_in():
	for msg in live_in:
		if msg.type == 'control_change':
			print(msg.control,msg.value)
		apc_out.send(msg)
Thread(target=live_loop_in).start()