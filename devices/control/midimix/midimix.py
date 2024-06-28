	# Akai Midimix setup

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
				12:[910,{}],
				13:[909,{}],
				14:[900,{}],
				15:[911,{}],
			},
			100:{},
			101:{
				8:[120,{}],
				9:[121,{}],
			},
			102:{
				8:[376,{}],
				9:[377,{}],
				10:[378,{}],
				11:[379,{}],
			},
		},
		1:{
			'common':{},
			102:{
				8:[382,{}],
				9:[383,{}],
				14:[380,{}],
				15:[381,{}],
			},
		},
		2:{
			'common':{},
			102:{
				8:[382,{}],
				9:[383,{}],
		}
		},
		3:{
			'common':{},
		},
	})

	# Add menus to layouts
	for _ in range(400,408):
		self.default_layout['all'][1]['common'].update({_-392:[_,{}]})
	
	# Add encoders to display
	for _ in range(200,232):
		self.default_layout['all'][0]['common'].update({_:[_,{}]})

	
	# Add fader buttons
	for _ in range(300,308):
		self.default_layout['all'][0]['common'].update({_-300:[_,{}]})
	
	# Add Plugins action buttons
	for _ in range(260,268):
		self.default_layout['all'][0][102].update({_-244:[_,{}]})
	
	# Add Plugins selection buttons
	for _ in range(16):
		self.default_layout['all'][1][102].update({_+48:[_+360,{}]})
	
going_out = {
	'cc':{},
	'nt':{
		### Don't modify 25 and 26 since it's the layouts buttons
		(25,0):[922,[]],
		(26,0):[921,[]],
		
	},
	'pw':{},
}

getting_in = {}

count = 0
for _ in[3,6,9,12,15,18,21,24,1,4,7,10,13,16,19,22,2,5,8,11,14,17,20,23]:
	going_out['nt'].update({(_,0):[count,[]]})
	getting_in.update({count:[{'model':'nt'},_]})
	count += 1

count = 200
for _ in[19,23,27,31,49,53,57,61,18,22,26,30,48,52,56,60,17,21,25,29,47,51,55,59,16,20,24,28,46,50,54,58]:
	going_out['cc'].update({(_,0):[count,{'model':'cc','pickup':{'grab_zone':2,'tolerance':2}}]})
	count += 1

def pre_midi(self,msg):
	if msg.type == 'note_on' and msg.note == 27:
		speak("Set 2")

data = {
	'name' : "Akai Midi Mix",
	'ports':['MIDI Mix','MIDI Mix','startswith'],
	'toggle_type':1,
	'fre_count':32,
	'getting_in':getting_in,
	'going_out':going_out,
	'control_init':[control_init],
	'pre_midi':[pre_midi,True],
	'colors':{

		# Common to all daws
		'off':0,
		'on':127,
		'dim1':0,
		'dim2':0,
		'red':127,
		'blue':127,
		'green':127,
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
		'send_sel_on':127,
		'send_sel_off':0,
		'recv_sel_on':127,
		'recv_sel_off':0,

		# Plugins
		'plugins_pagenav_on':127,
		'plugins_pagenav_off':0,
		'plugins_plugnav_on':127,
		'plugins_plugnav_off':0,
		'plugins_pt_user_on':127,
		'plugins_pt_user_off':0,
		'plugins_pt_8banks_on':127,
		'plugins_pt_8banks_off':0,
		'plugins_plugsel_on':127,
		'plugins_plugsel_off':0,

		# Plugins User buttons
		'plugins_usrbtn_param_on':127,
		'plugins_usrbtn_param_off':0,
		'plugins_usrbtn_cc_on':127,
		'plugins_usrbtn_cc_off':0,
		'plugins_usrbtn_nt_on':127,
		'plugins_usrbtn_nt_off':0,
		'plugins_usrbtn_osc_on':127,
		'plugins_usrbtn_osc_off':0,
		'plugins_usrbtn_mouse_on':127,
		'plugins_usrbtn_mouse_off':0,

		# Control modes
		
		# Drum Rack
		'modes_dr_on':17,
		'modes_dr_regular':14,
		
		# Scaled pads
		'modes_sp_dim':0,
		'modes_sp_on':127,
		'modes_sp_root':127,
		'modes_sp_scale':127,
		
		# Transport
		'tr_stop_on':127,
		'tr_stop_off':0,
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