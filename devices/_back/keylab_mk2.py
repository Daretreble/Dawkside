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
		'permanent':{},
		0:{
			'common':{
				93:[1,93,{}],
				94:[1,94,{}],
				95:[1,95,{}],
				96:[1,102,{}],
			},
			100:{},
			101:{},
			102:{},
			130:{},
			131:{
				140:[1,868,{}],
				141:[1,869,{}],
				251:[1,251,{'type':'scale_nav'}],
			},
		},
		1:{
			'common':{
				99:[1,81,{}],
			},
		},
		2:{
			102:{
				80:[94.{}],
			},
		},
		3:{
			'common':{},
		},
	})

	# Add encoders to display
	for _ in range(200,208):
		self.default_layout['all'][0]['common'].update({_:[1,_,{}]})

	# Add menus to layouts
	for _ in range(400,408):
		self.default_layout['all'][0]['common'].update({_-330:[1,_,{}]})
	for _ in range(410,410+len(self.main.outmodes)):
		self.default_layout['all'][1]['common'].update({_-340:[1,_,{}]})
	for _ in range(430,430+len(self.modes.sections)):
		self.default_layout['all'][2]['common'].update({_-360:[1,_,{}]})
	for _ in range(420,424):
		self.default_layout['all'][3]['common'].update({_-350:[1,_,{}]})
	
	# Add fader buttons
	for _ in range(300,308):
		self.default_layout['all'][0]['common'].update({_-220:[1,_,{}]})
	
	# Add Plugins action buttons
	for _ in range(32):
		self.default_layout['all'][0][102].update({_	:[1,_+260,{}]})
	
	# Add Plugins selection buttons
	
	for _ in range(16):
		self.default_layout['all'][0][102].update({_+48:[1,_+360,{}]})
	
	# Add modes matrix
	for i in range(130,132):
		self.default_layout['all'][0][i].update({136:[1,866,{}]})
		self.default_layout['all'][0][i].update({137:[1,867,{}]})
		self.default_layout['all'][0][i].update({138:[1,864,{}]})
		self.default_layout['all'][0][i].update({139:[1,865,{}]})
		for j in range(64):
			self.default_layout['all'][0][i].update({j:[1,j+800,{}]})

def pre_midi(self,msg):
	
	if msg.type in['note_on','note_off'] and msg.channel == 9:
		if msg.type == 'note_on':
			msg.velocity = 127
		else:
			msg.velocity = 0

	if msg.type == 'pitchwheel':
		if msg.pitch < -8100:
			msg.pitch = -8192
		elif msg.pitch > 8100:
			msg.pitch = 8191
	
	if msg.type == 'sysex':

		passed = False
		if len(msg.data) == 10 and (msg.data == (0,32,107,127,66,2,0,0,21,0) or msg.data== (0,32,107,127,66,2,0,0,21,127)):
			if msg.data[9] == 0:
				self.matrix_in(action='full')
				speak("Dawkside mode")
			else:
				speak('User or Analog Lab modes')


going_out = {
	'cc':{},
	'nt':{
		### Don't modify 48 and 49 since they're the layouts buttons
		(8,0):[921,[]],
		(16,0):[922,[]],
		(91,0):[91,[]],
		(92,0):[92,[]],
		(93,0):[93,[]],
		(94,0):[94,[]],
		(94,0):[94,[]],
		(95,0):[95,[]],
		(86,0):[96,[]],

	},
	'pw':{},
}

getting_in = {
	91:[{'model':'sy'},106],
	92:[{'model':'sy'},107],
	93:[{'model':'sy'},108],
	94:[{'model':'sy'},109],
	95:[{'model':'sy'},110],
	96:[{'model':'sy'},111],
	
	103:[{'model':'sy'},104],
}

data = {
	'type':'control',
	'name' : "Arturia KeyLab Mk2",
	'ports':['MIDIIN2 (KeyLab mkII 61)','MIDIOUT2 (KeyLab mkII 61)'],
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