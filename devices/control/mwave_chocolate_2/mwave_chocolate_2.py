# Arturia KeyLab Mk2

from mido import Message as MidiMsg
from functions.speak import speak

def control_init(self):

	# Generate layouts
	self.default_layout = {
		'all':{},
		'reaper':{},
		'live':{}
	}

	

def pre_midi(self,msg):
	
		print(msg)

going_out = {
	'cc':{
		(0,0):[94,[]],
	},
	'nt':{},
	'pw':{},
}

data = {
	'type':'control',
	'name' : "mWave Chocolate",
	'ports':['USB-Midi',False],
	'going_out':going_out,
	'control_init':[control_init]
}