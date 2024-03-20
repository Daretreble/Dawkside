# Icon Platform X+ setup

from mido import Message as MidiMsg

def control_init(self):

	# Generate layouts
	self.default_layout = {
		'all':{},
		'reaper':{},
		'live':{}
	}

	# Common defaults
	self.default_layout['all'].update({
		'permanent':{},
		0:{
			'common':{
				75:[911,{}],
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
				70:[120,{}],
				71:[121,{}],
			},
			102:{
				70:[376,{}],
				71:[377,{}],
				72:[378,{}],
				73:[379,{}],
				74:[910,{}],
				251:[251,{'type':'param_nav'}],
			},
		},
		1:{
			'common':{
				15:[401,{}],
				23:[402,{}],
				31:[403,{}],
				75:[910,{}],
			},
			102:{
				70:[380,{}],
				71:[381,{}],
				207:[251,{'type':'param_nav'}],
			}
		},
		2:{
			'common':{
				15:[420,{}],
				23:[421,{}],
				31:[422,{}],
			},
		},
		3:{
			'common':{},
		},
	})

	# Add encoders to display
	for _ in range(200,208):
		self.default_layout['all'][0]['common'].update({_:[_,{}]})
	
going_out = {
	'cc':{},
	'nt':{
		### Don't modify 38 and 39 since they're the layouts buttons
		(39,0):[921,[]],
				(38,0):[922,[]],
	},
	'pw':{},
}

getting_in = {}

# (70-76) First 6 encoders press
for _ in range(70,76):
	going_out['nt'].update({(_-38,0):[_,[]]})

# (0-32) All buttons from bottom to top
for _ in range(8,32):
	going_out['nt'].update({(_,0):[_,[]]})
	getting_in.update({_:[{'model':'nt'},_]})

# (200,207) First 8 faders
for _ in range(200,208):
	going_out['pw'].update({(_-200):[_,{'model':'p1'}]})
	going_out['cc'].update({(_-184,0):[_,{'model':'r2'}]})
	getting_in.update({_:[{'model':'p1'},_-200]})
for _ in range(300,308):
	going_out['nt'].update({(_-196,0):[_,[]]})
	going_out['nt'].update({(_-300,0):[_,[]]})
	getting_in.update({_:[{'model':'nt'},_-300]})

def pre_midi(self,msg):
	
	if msg.type == 'pitchwheel':
		if msg.pitch > 8100:
			msg.pitch = 8191
		if msg.pitch < -8100:
			msg.pitch = -8192

data = {
	'name' : "Icon Platform X+",
	'ports':['Platform X+','Platform X+','startswith'],
	'mode':101,
	'outmode':11,
	'fre_count':16,
	'getting_in':getting_in,
	'going_out':going_out,
	'control_init':[control_init],
	'pre_midi':[pre_midi,True],
	'colors':{

		# Common to all daws
		'off':0,
		'on':1,
		'dim1':0,
		'dim2':0,
		'red':5,
		'blue':17,
		'green':27,
		'yellow':127,

		# Menus
		'daw_modes_on':127,
		'daw_modes_off':0,
		'daw_modes_dim':0,
		'daw_select_on':127,
		'daw_select_off':0,
		'daw_select_dim':0,

		# Faders and encoders buttons
		'fre_param_on':127,
		'fre_param_off':0,
		'fre_send_on':127,
		'fre_send_off':0,
		'fre_recv_on':127,
		'fre_recv_off':0,
		'fre_volume':127,
		'fre_pan':127,
		
		# Send and receive buttons
		'send_sel_on':6,
		'send_sel_off':5,
		'recv_sel_on':6,
		'recv_sel_off':5,

		# Plugins
		'plugins_pagenav_on':6,
		'plugins_pagenav_off':5,
		'plugins_plugnav_on':6,
		'plugins_plugnav_off':5,
		'plugins_pt_user_on':6,
		'plugins_pt_user_off':5,
		'plugins_pt_8banks_on':6,
		'plugins_pt_8banks_off':5,
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