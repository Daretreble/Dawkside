# Arturia Minilab 3

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
				93:[93,{}],
				94:[94,{}],
				95:[95,{}],
				96:[102,{}],
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
	
def pre_midi(self,msg):
	
	if msg.type == 'sysex':

		passed = False
		if msg.data == (0,32,107,127,66,2,0,64,98,1):
			self.routing_destination = self.daw.routing
			speak("Analog Lab mode")
		if msg.data == (0,32,107,127,66,2,0,64,98,2):
			self.routing_destination = False
			speak("Daw mode")
		if msg.data == (0,32,107,127,66,2,0,64,98,3):
			self.routing_destination = False
			speak("Dawkside mode")
		if msg.data == (0,32,107,127,66,2,0,64,99,0):
			speak ("Bank 1")
		if msg.data == (0,32,107,127,66,2,0,64,99,1):
			speak ("Bank 2")


going_out = {
	'cc':{
		### Don't modify 9 since it's the layouts button
		(27,0):[921,[]],
	},
	'nt':{},
	'pw':{},
}

getting_in = {}

# (200,207) Encoders
count = 200
for _ in [110,111,116,117,86,87,89,90]:
	going_out['cc'].update({(_,0):[_,{'model':'r1'}]})
	count += 1

data = {
	'name' : "Arturia KeyLab Mk2",
	'ports':['Minilab3','Minilab3'],
	'touch_tolerance':20,
	'getting_in':getting_in,
	'going_out':going_out,
	'control_init':[control_init],
	'pre_midi':[pre_midi,True],
	'colors':{

			# Common to all daws
			'off':[8,[0,32,107,127,66,2,0,22,0,0,0,0]],
			'on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'dim1':[8,[0,32,107,127,66,2,0,22,0,0,0,0]],
			'dim2':[8,[0,32,107,127,66,2,0,22,0,0,0,0]],
			'red':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'blue':[8,[0,32,107,127,66,2,0,22,0,0,0,127]],
			'green':[8,[0,32,107,127,66,2,0,22,0,0,127,0]],
			'yellow':[8,[0,32,107,127,66,2,0,22,0,127,127,0]],

			# Menus
			'daw_modes_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'daw_modes_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'daw_modes_dim':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'control_modes_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'control_modes_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'control_modes_dim':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'output_modes_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'output_modes_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'output_modes_dim':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'daw_select_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'daw_select_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'daw_select_dim':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],

			# Faders and encoders buttons
			'fre_param_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'fre_param_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'fre_send_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'fre_send_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'fre_recv_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'fre_recv_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'fre_volume':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'fre_pan':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			
			# Send and receive buttons
			'send_sel_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'send_sel_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'recv_sel_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'recv_sel_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],

			# Plugins
			'plugins_pagenav_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'plugins_pagenav_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'plugins_plugnav_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'plugins_plugnav_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'plugins_pt_user_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'plugins_pt_user_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'plugins_pt_8banks_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'plugins_pt_8banks_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],
			'plugins_plugsel_on':[8,[0,32,107,127,66,2,0,22,0,127,127,127]],
			'plugins_plugsel_off':[8,[0,32,107,127,66,2,0,22,0,127,0,0]],

			# Transport
			'tr_stop_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_stop_off':[8,[0,32,107,127,66,2,0,16,0,40]],
			'tr_play_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_play_off':[8,[0,32,107,127,66,2,0,16,0,40]],
			'tr_record_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_record_off':[8,[0,32,107,127,66,2,0,16,0,40]],
			'tr_repeat_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_repeat_off':[8,[0,32,107,127,66,2,0,16,0,40]],
			'tr_metronome_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_metronome_off':[8,[0,32,107,127,66,2,0,16,0,40]],
			'tr_readwrite_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_readwrite_off':[8,[0,32,107,127,66,2,0,16,0,40]],

			},
		

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