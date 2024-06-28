# Akai APC Mini setup
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
			110:[911,{}],
			111:[910,{}],
			112:[909,{}],
			113:[900,{}],			
			117:[999,{}],			
		},
		0:{
			'common':{},
			100:{
				8:[105,{}],
				9:[106,{}],
			},
			101:{
				8:[120,{}],
				9:[121,{}],
			},
			102:{
				8:[376,{}],
				9:[377,{}],
				10:[378,{}],
				11:[379,{}],
				14:[380,{}],
				15:[381,{}],
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
			102:{
				8:[382,{}],
				9:[383,{}],
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

	#for _ in range(430,430+len(self.modes.sections)):
		#self.default_layout['all'][2]['common'].update({_-360:[_,{}]})
	#for _ in range(420,424):
		#self.default_layout['all'][3]['common'].update({_-350:[_,{}]})
	
	# AddMenus
	for _ in range(400,408):
		self.default_layout['all'][0]['common'].update({_-330:[_,{}]})
	
	# Add fader buttons
	for _ in range(300,308):
		self.default_layout['all'][0]['common'].update({_-300:[_,{}]})
	
	# Add Plugins selection buttons
	for _ in range(360,368):
		self.default_layout['all'][0][102].update({_-344:[_,{}]})

	# Add Plugins action buttons
	for _ in range(260,292):
		self.default_layout['all'][0][102].update({_-228:[_,{}]})
	
	# Add modes matrix
	for i in range(130,132):
		self.default_layout['all'][0][i].update({136:[866,{}]})
		self.default_layout['all'][0][i].update({137:[867,{}]})
		self.default_layout['all'][0][i].update({138:[864,{}]})
		self.default_layout['all'][0][i].update({139:[865,{}]})
		for j in range(64):
			self.default_layout['all'][0][i].update({j:[j+800,{}]})
	
	
going_out = {
	'cc':{},
	'nt':{
		### Don't modify 98 since they're the layouts buttons
		(98,0):[921,[]],
	},
	'pw':{},
}

getting_in = {}

# (0-63) Add 64 pads
for r in range(56,-8,-8):
	for c in range(8):
		going_out['nt'].update({(c+r,0):[c+r,[]]})
		getting_in.update({c+r:[{'model':'nt'},c+r]})

# (70-77) Add the 8 buttons located directly underneath the 64 pads.
for _ in range(70,78):
	going_out['nt'].update({(_-6,0):[_,[]]})
	getting_in.update({_:[{'model':'nt'},_-6]})

# 110-117) Add the 8 buttons on the right, from bottom to top.
count = 110
for _ in range(89,81,-1):
	going_out['nt'].update({(_,0):[count,[]]})
	getting_in.update({count:[{'model':'nt'},_]})
	count += 1

# (200,207) First 8 faders
for _ in range(200,208):
	going_out['cc'].update({(_-152,0):[_,{'model':'cc','pickup':{'grab_zone':2,'tolerance':2}}]})

def pre_midi(self,msg):

	pass
	"""
	if msg.type == 'control_change' and msg.control == 56:
		value = round(msg.value/127,4)
		self.daw.client.send_message('/live/device/set/parameter/value',(0,0,3,value))
	"""
	
data = {
	'name' : "Akai APC Mini",
	'ports':['APC MINI','APC MINI','startswith'],
	'toggle_type':1,
	'getting_in':getting_in,
	'going_out':going_out,
	'control_init':[control_init],
	'pre_midi':[pre_midi,True],
	'colors':{

		# Ableton Live
		'clip_stopped':5,
		'clip_playing':1,
		'clip_fired':3,
		
		# Common to all daws
		'off':0,
		'on':1,
		'dim1':0,
		'dim2':0,
		'red':3,
		'blue':1,
		'green':1,
		'yellow':5,

		# Menus
		'daw_modes_on':2,
		'daw_modes_off':0,
		'daw_modes_dim':1,
		'control_modes_on':2,
		'control_modes_off':0,
		'control_modes_dim':1,
		'output_modes_on':2,
		'output_modes_off':0,
		'output_modes_dim':1,
		'daw_select_on':2,
		'daw_select_off':0,
		'daw_select_dim':1,

		# Faders and encoders buttons
		'fre_param_on':4,
		'fre_param_off':0,
		'fre_send_on':4,
		'fre_send_off':0,
		'fre_recv_on':4,
		'fre_recv_off':0,
		'fre_volume':5,
		'fre_pan':1,
		
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
		'plugins_usrbtn_param_off':3,
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