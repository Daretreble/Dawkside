import time
import pyautogui
import subprocess
import os
import pprint
from threading import Thread
from mido import Message as MidiMsg
from functions.speak import speak
from functions.command_common import command_common

def exec(self,**kwargs):

	control = self.control
	daw = self.control.daw
	main = daw.main
	plugins = daw.plugins
	user = plugins.user

	button_type = kwargs['button_type']
	pos = kwargs['pos']
	velo = kwargs['velocity']
	state = kwargs['state']

	passed = False

	def action_exec(seq):

		event_type = seq['event_type']

		# Command
		if event_type == 'command':
			command = seq['id']
			command_common(daw,control,command,[[command, []], True, velo],{})
		
		# Plugin parameter
		if event_type == 'plugin_param':
			daw.client.send_message(f"/fxparam/{seq['param_id']}/value",seq['value'])
		
		# Midi cc
		if event_type == 'midi_cc':
			daw.routing.midiout(MidiMsg('control_change',control=seq['control'],channel=seq['channel'],value=seq['value']))
		
		# Midi note
		if event_type == 'midi_note':
			if seq['velocity']:
				daw.routing.midiout(MidiMsg('note_on' if seq['velocity'] > 0 else 'note_off',note=seq['note'],channel=seq['channel'],velocity=seq['velocity']))
			else:
				daw.routing.midiout(MidiMsg('note_on' if velo > 0 else 'note_off',note=seq['note'],channel=seq['channel'],velocity=velo))
			
		
		# OSC Message
		if event_type == 'osc':
			arguments = seq['arguments']
			print(arguments,type(arguments))
			daw.client.send_message(seq['message'],arguments)

		if event_type == 'mouse':
			event_data = False
			if isinstance(seq['event'],list):
				event_tmp = seq['event'][0]
				event_data = seq['event'][1]
			else:
				event_tmp = seq['event']
			if event_tmp == 'move':
				pyautogui.moveTo(event_data[0],event_data[1])
			if event_tmp == 'left_click':
				pyautogui.click()
			if event_tmp == 'right_click':
				pyautogui.click(button='right')
			if event_tmp == 'double_click':
				pyautogui.click(clicks=2, interval=0.1)

		# Application launch
		if event_type == 'app':

			### Personal notes for ControlMyMonitor.exe
			### Change input for ASUS : /SetValue Primary 60 17

			app_name = os.path.join('apps',seq['name'])
			app_arguments = seq['arguments']
			subprocess.Popen(app_name + app_arguments, shell=True)



	button_action = False
	if button_type == 'user':
		orig = control.matrix['commands'][pos]
	if button_type == 'plugin_button':
		orig = btn = plugins.user_params[plugins.name][plugins.page[0]][button_type][pos]
	latch_on = True if 'options' in orig and 'latch' in orig['options'] else False
	if latch_on:
		if ('pressed' in orig and 'released' in orig) and orig['pressed'][0]['event_type'] == 'plugin_param':
			if state:
				
				value_on = orig['pressed'][0]['value']
				value_off = orig['released'][0]['value']
				value_actual = plugins.params[orig['pressed'][0]['param_id']]['val']
				
				if value_actual < value_on:
					value_sent = value_on
				else:
					value_sent = value_off
				
				daw.client.send_message(f"/fxparam/{orig['pressed'][0]['param_id']}/value",value_sent)
		else:
			if state:
				if orig['options']['latch']['state']:
					button_action = 'released'
					orig['options']['latch']['state'] = False
				else:
					button_action = 'pressed'
					orig['options']['latch']['state'] = True
				passed = True
			else:
				passed = False
	else:
		button_action = 'pressed' if state else 'released'
		passed = True
	
	if button_action and button_action in orig and passed:
		btn = orig[button_action]
		passed = True
	else:
		passed = False

	if passed:

		def to_execute():

			for seq in btn:

				if 'time_out' in seq:
					time.sleep(seq['time_out']/1000)
				
				action_exec(seq)

		if len(btn) > 1:
			Thread(target=to_execute).start()
		else:
			to_execute()

