# Ableton Push 1 setup

from mido import Message as MidiMsg

def control_init(self):

	# Generate layouts
	self.default_layout = {
		'all':{},
		'reaper':{},
		'live':{}
	}

	# Live defaults
	self.default_layout['live'].update({
		0:{
			'common':{},
			100:{},
		},
	})
	count = 1000
	for row in range(56,-8,-8):
		for col in range(8):
			self.default_layout['live'][0][100][col+row] = [count,{}]
			count += 1
	
	# Common defaults
	self.default_layout['all'].update({
		'permanent':{
			132:[910,{}],
			133:[911,{}],
			134:[909,{}],
			135:[900,{}],
			136:[999,{}],
			
		},
		0:{
			'common':{
				100:[98,{}],
				99:[80,{}],
				91:[95,{}],
				90:[94,{}],
				300:[300,{}],
				301:[301,{}],
				302:[302,{}],
				303:[303,{}],
				304:[304,{}],
				305:[305,{}],
				306:[306,{}],
				307:[307,{}],
			},
			100:{},
			101:{
				56:[120,{}],
				57:[121,{}],
			},
			102:{
				40:[380,{}],
				41:[381,{}],
				122:[376,{}],
				123:[377,{}],
				120:[378,{}],
				121:[379,{}],
				251:[251,{'type':'param_nav'}],
			},
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
		self.default_layout['all'][0]['common'].update({_-330:[_,{}]})
	for _ in range(410,410+len(self.main.outmodes)):
		self.default_layout['all'][1]['common'].update({_-340:[_,{}]})
	for _ in range(430,430+len(self.modes.sections)):
		self.default_layout['all'][2]['common'].update({_-360:[_,{}]})
	for _ in range(420,424):
		self.default_layout['all'][3]['common'].update({_-350:[_,{}]})
	
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
		
	# Set Push Touch Strip mode to Pitchbend no return
	self.port.midiout(MidiMsg('sysex',data=[71,127,21,99,0,1,1]))

	# Set Push pad sensitivity
	#self.port.midiout(MidiMsg('sysex',data=[71,127,21,93]))
	#240,71,127,21,93...,247

going_out = {
	'cc':{
		### Don't modify 48 and 49 since they're the layouts buttons
		(48,0):[921,[]],
		(49,0):[922,[]],
		(14,0):[251,{'model':'r1'}],
		(15,0):[252,{'model':'r1'}],
	},
	'nt':{},
	'pw':{},
}

getting_in = {}

# (0-63) Add 64 pads
for _ in range(64):
	going_out['nt'].update({(_+36,0):[_,[]]})
	getting_in.update({_:[{'model':'nt'},_+36]})

# (300,307) Add the first 8 encoders touch
for _ in range(300,308):
	going_out['nt'].update({(_-300,0):[_,[]]})

# (70-77) Add the 8 buttons located directly over the 64 pads.
for _ in range(70,78):
	going_out['cc'].update({(_+32,0):[_,[]]})
	getting_in.update({_:[{'model':'cc'},_+32]})

# (80-87) Add the 8 buttons at the top of the middle section
for _ in range(80,88):
	going_out['cc'].update({(_-60,0):[_,[]]})
	getting_in.update({_:[{'model':'cc'},_-60]})

cc_btns = [
	## (90-101) Left side of 64 pads, from bottom to top
	[101,3],
	[100,9],
	[99,119],
	[98,118],
	[97,117],
	[96,116],
	[95,90],
	[94,89],
	[93,88],
	[92,87],
	[91,86],
	[90,85],

	## (110-119) column of buttons on the right of the 64 pads, bottom to top
	[119,28],
	[118,29],
	[117,43],
	[116,42],
	[115,41],
	[114,40],
	[113,39],
	[112,38],
	[111,37],
	[110,36],

	## (120-123) Directional buttons
	[120,47],
	[121,46],
	[122,44],
	[123,45],

	## (132-151) Buttons on the right side, bottom to top, left to right (zigzag)
	[132,50],
	[133,51],
	[134,52],
	[135,53],
	[136,54],
	[137,55],
	[138,56],
	[139,57],
	[140,58],
	[141,59],
	[142,60],
	[143,61],
	[144,62],
	[145,110],
	[146,111],
	[147,112],
	[148,113],
	[149,114],
	[150,115],
]
for _ in cc_btns:
	going_out['cc'].update({(_[1],0):[_[0],[]]})
	getting_in.update({ _[0]:[{'model':'cc'},_[1]],  })

# (200,207) First 8 faders
for _ in range(200,208):
	going_out['cc'].update({(_-129,0):[_,{'model':'r1'}]})

data = {
	'name' : "Ableton Push 1",
	'ports':['MIDIIN2 (Ableton Push)','MIDIOUT2 (Ableton Push)','startswith'],
	'touch_tolerance':20,
	'getting_in':getting_in,
	'going_out':going_out,
	'control_init':[control_init],
	'colors':{

		# Ableton Live
		'clip_stopped':17,
		'clip_playing':[[[0,0],[17,9]]],
		'clip_fired':[[[0,0],[5,9]]],
		
		# Common to all daws
		'off':0,
		'on':127,
		'dim1':1,
		'dim2':6,
		'red':5,
		'blue':17,
		'green':27,
		'yellow':127,

		# Menus
		'daw_modes_on':13,
		'daw_modes_off':0,
		'daw_modes_dim':26,
		'control_modes_on':13,
		'control_modes_off':0,
		'control_modes_dim':26,
		'output_modes_on':13,
		'output_modes_off':0,
		'output_modes_dim':26,
		'daw_select_on':26,
		'daw_select_off':0,
		'daw_select_dim':13,

		# Faders and encoders buttons
		'fre_param_on':4,
		'fre_param_off':1,
		'fre_send_on':4,
		'fre_send_off':1,
		'fre_recv_on':4,
		'fre_recv_off':1,
		'fre_volume':41,
		'fre_pan':41,
		
		# Send and receive buttons
		'send_sel_on':13,
		'send_sel_off':14,
		'recv_sel_on':13,
		'recv_sel_off':14,

		# Plugins
		'plugins_pagenav_on':13,
		'plugins_pagenav_off':14,
		'plugins_plugnav_on':13,
		'plugins_plugnav_off':14,
		'plugins_pt_user_on':13,
		'plugins_pt_user_off':14,
		'plugins_pt_8banks_on':13,
		'plugins_pt_8banks_off':14,
		'plugins_plugsel_on':13,
		'plugins_plugsel_off':14,

		# Plugins User buttons
		'plugins_usrbtn_param_on':5,
		'plugins_usrbtn_param_off':6,
		'plugins_usrbtn_cc_on':5,
		'plugins_usrbtn_cc_off':6,
		'plugins_usrbtn_nt_on':5,
		'plugins_usrbtn_nt_off':6,
		'plugins_usrbtn_osc_on':5,
		'plugins_usrbtn_osc_off':6,
		'plugins_usrbtn_mouse_on':5,
		'plugins_usrbtn_mouse_off':6,

		# Control modes
		
		# Drum Rack
		'modes_dr_on':17,
		'modes_dr_regular':14,
		
		# Scaled pads
		'modes_sp_dim':1,
		'modes_sp_on':17,
		'modes_sp_root':60,
		'modes_sp_scale':14,
		
		# Transport
		'tr_stop_on':6,
		'tr_stop_off':5,
		'tr_play_on':6,
		'tr_play_off':7,
		'tr_record_on':6,
		'tr_record_off':7,
		'tr_repeat_on':4,
		'tr_repeat_off':5,
		'tr_metronome_on':4,
		'tr_metronome_off':5,
		'tr_readwrite_on':4,
		'tr_readwrite_off':5,

	}
}