# mWave Chocolate foot controller

from mido import Message as MidiMsg
from functions.speak import speak

def control_init(self):

	# Generate layouts
	self.default_layout = {
		'all':{},
		'reaper':{},
		'live':{}
	}

	# Reaper defaults
	self.default_layout['reaper'].update({
		0:{
			'common':{
				0:[95,{}],
				1:[80,{}],
				10:[95,{}],
				11:[98,{}],
			}
		},
		1:{
			'common':{
				0:[93,{}],
			}
		},
	})

	# Live defaults
	self.default_layout['live'].update({
		0:{
			'common':{
				0:[1100,{}],
				1:[1090,{}],
				2:[104,{}],
				3:[1100,{}],
				4:[98,{}],
				5:[98,{}],
				6:[104,{}],
				7:[98,{}],
			}
		},
		1:{
			'common':{
				0:[1100,{}],
				10:[1100,{}],
			}
		},
	})
	
def pre_midi(self,msg):
	
	"""if msg.control == 3:
		self.disp_toggle = True
	elif msg.control != 13:
		self.disp_toggle = False

	if self.disp_toggle:
		self.layout_active = 1
	else:
		self.layout_active = 0"""

going_out = {
	'cc':{
		(0,0):[0,[]],
		(10,0):[1,[]],
		(1,0):[2,[]],
		(11,0):[3,{'state':True}],
		(2,0):[4,[]],
		(12,0):[5,[]],
		(3,0):[6,[]],
		(13,0):[7,{'state':False}],
	},
	'nt':{},
	'pw':{},
}

data = {
	'name' : "mWave Chocolate",
	'ports':['USB-Midi',False,'startswith'],
	'going_out':going_out,
	'control_init':[control_init],
	'pre_midi':[pre_midi,True],
	'disp_toggle':False,
}