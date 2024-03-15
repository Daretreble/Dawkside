import os
import importlib
import mido
import mido.backends.rtmidi
import pprint

from classes.control.control import Control
from classes.keys.keys import Keys
from classes.ports.ports import Ports

def device_loader(main):
	""" Initializes devices. """
	
	inports = mido.get_input_names()
	
	for cat in ['control', 'keys','ports']:
		folder_path = os.path.join('devices', cat)
		subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
		stripped_subfolders = [f for f in subfolders if f != '__pycache__']
		
		for d in stripped_subfolders:
			device_module = importlib.import_module(f"devices.{cat}.{d}.{d}")
			data = device_module.data
			data.update({'short_name': d})
			port = data['ports'][0]
			searching = data['ports'][2]
			linked_ports = []
			for _ in inports:
				if searching == 'startswith':
					linked_test = _.startswith(port)
				if searching == 'contains':
					linked_test = port in _
				if linked_test:
					inports.remove(_)
					linked_ports.append(_)
			#linked_ports = [item for item in inports if item.startswith(port)]
			
			if len(linked_ports) > 0:
				if cat == 'control':
					main.devices[cat][d] = Control(main, data)
				elif cat == 'keys':
					main.devices[cat][d] = Keys(main,data)
				elif cat == 'ports':
					main.devices[cat][d] = Ports(main,data)