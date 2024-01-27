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

	# Common defaults
	self.default_layout['all'].update({
		'permanent':{
			110:[900,{}],
			111:[911,{}],
			114:[909,{}],
			115:[910,{}],
		},
		0:{
			'common':{
				0:[1100,{}],
			},
			100:{},
			101:{},
			102:{},
			130:{},
			131:{
				140:[868,{}],
				141:[869,{}],
				251:[251,{'type':'scale_nav'}],
			},
		},
		1:{
			'common':{
				99:[81,{}],
			},
		},
		2:{
			'common':{},
		},
		3:{
			'common':{},
		},
	})

	# Add encoders to display
	for _ in range(200,208):
		self.default_layout['all'][0]['common'].update({_:[_,{}]})

	# Add menus to layouts
	for _ in range(400,408):
		self.default_layout['all'][1]['common'].update({_-320:[_,{}]})
	for _ in range(410,410+len(self.main.outmodes)):
		self.default_layout['all'][1]['common'].update({_-320:[_,{}]})
	
	# Add fader buttons
	for _ in range(300,308):
		self.default_layout['all'][0]['common'].update({_-220:[_,{}]})
	
	# Add Plugins action buttons
	for _ in range(32):
		self.default_layout['all'][0][102].update({_	:[_+260,{}]})
	
	# Add Plugins selection buttons
	
	for _ in range(16):
		self.default_layout['all'][0][102].update({_+48:[_+360,{}]})
	
	# Add modes matrix
	for i in range(130,132):
		self.default_layout['all'][0][i].update({136:[866,{}]})
		self.default_layout['all'][0][i].update({137:[867,{}]})
		self.default_layout['all'][0][i].update({138:[864,{}]})
		self.default_layout['all'][0][i].update({139:[865,{}]})
		for j in range(64):
			self.default_layout['all'][0][i].update({j:[j+800,{}]})

def pre_midi(self,msg):
	
		print(msg)

going_out = {
	'cc':{
		(0,0):[0,[]],
		
	},
	'nt':{},
	'pw':{},
}

data = {
	'name' : "mWave Chocolate",
	'ports':['USB-Midi',False],
	'going_out':going_out,
	'control_init':[control_init]
}