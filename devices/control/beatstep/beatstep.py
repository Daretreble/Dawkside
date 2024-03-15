# Arturia Beatstep (original)

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
		'permanent':{},
		0:{
			'common':{
				100:[900,{}],
			},
			100:{
				70:[94,{}],
				71:[98,{}],
				76:[104,{}],
				77:[95,{}],
			},
			101:{},
			102:{
				70:[376,{}],
				71:[377,{}],
				72:[378,{}],
				73:[379,{}],
			},
		},
		1:{
			'common':{},
		},
		2:{
			'common':{
				80:[376,{}],
				81:[377,{}],
				82:[378,{}],
				83:[379,{}],
			},
			102:{
				88:[381,{}],
			},
		},
		3:{
			'common':{},
		},
	})

	


def pre_midi(self,msg):
	
	if msg.type == 'control_change':
		value = msg.value
		if value in range(0,65):
			msg.value = 4
		elif value in range(65,128):
			msg.value = 123
		
	
	#if msg.type == 'clock':
		#passed = True

	# Add menus to layouts
	for _ in range(400,408):
		self.default_layout['all'][1]['common'].update({_-322:[_,{}]})
	
	# Add fader buttons
	for _ in range(300,308):
		self.default_layout['all'][0]['common'].update({_-222:[_,{}]})
	
	# Add encoders to display
	for _ in range(200,208):
		self.default_layout['all'][0]['common'].update({_:[_,{}]})

going_out = {
	'cc':{},
	'nt':{
		### Don't modify 1 since it's the layout button.
		(1,0):[921,[]],
		(2,0):[100,[]],
	},
	'pw':{},
}

# (200,207) First 8 faders
for _ in range(200,208):
	going_out['cc'].update({(_-100,0):[_,{'model':'r1'}]})

# 16 pads
for _ in range(70,86):
	going_out['nt'][(_-58,0)] = [_,[]]

getting_in = {}
for _ in range(70,86):
	getting_in.update({_:[{'model':'nt'},_-34]})

data = {
	'name' : "Arturia Beatstep",
	'ports':['Arturia BeatStep','Arturia BeatStep','startswith'],
	'going_out':going_out,
	'getting_in':getting_in,
	'control_init':[control_init],
	'pre_midi':[pre_midi,True],
	'colors':{

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
		'daw_modes_on':127,
		'daw_modes_off':0,
		'daw_modes_dim':0,
		'control_modes_on':127,
		'control_modes_off':0,
		'control_modes_dim':0,
		'output_modes_on':127,
		'output_modes_off':0,
		'output_modes_dim':0,
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
		'send_sel_on':13,
		'send_sel_off':14,
		'recv_sel_on':13,
		'recv_sel_off':14,

		# Plugins
		'plugins_pagenav_on':127,
		'plugins_pagenav_off':127,
		'plugins_plugnav_on':127,
		'plugins_plugnav_off':0,
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
		'tr_play_on':127,
		'tr_play_off':0,
		'tr_record_on':127,
		'tr_record_off':0,
		'tr_repeat_on':127,
		'tr_repeat_off':0,
		'tr_metronome_on':127,
		'tr_metronome_off':0,
		'tr_readwrite_on':127,
		'tr_readwrite_off':0,

	}
}