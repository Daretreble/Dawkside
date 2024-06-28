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

	# Reaper defaults
	self.default_layout['reaper'].update({
		0:{
			'common':{
				501:[94,{}],
				502:[94,{}],
				503:[94,{}],
			}
		},
	})
	
	# Live defaults
	self.default_layout['live'].update({
		0:{
			'common':{
				91:[1090,{}],
				92:[1091,{}],
				110:[1070,{'pos':0}],
				111:[1070,{'pos':1}],
				112:[1070,{'pos':2}],
				113:[1070,{'pos':3}],
				114:[1070,{'pos':4}],
				115:[1070,{'pos':5}],
				116:[1070,{'pos':6}],
				117:[1070,{'pos':7}],
				501:[1100,{}],
				502:[1090,{}],
				503:[104,{}],
			}
		},
	})

	# Common defaults
	self.default_layout['all'].update({
		'permanent':{
			120:[910,{}],
			121:[909,{}],
			122:[911,{}],
		},
		0:{
			'common':{
				70:[72,{}],
				71:[71,{}],
				72:[70,{}],
				73:[105,{}],
				75:[900,{}],
				76:[80,{}],
				77:[104,{}],
				79:[98,{}],
				93:[93,{}],
				94:[94,{}],
				95:[95,{}],
				130:[105,{}],
				131:[106,{}],

			},
			100:{
				251:[251,{'type':'scene_nav'}],
			},
			101:{},
			102:{
				80:[376,{}],
				81:[377,{}],
				82:[360,{}],
				83:[361,{}],
				84:[362,{}],
				85:[363,{}],
				86:[364,{}],
				87:[365,{}],
				251:[251,{'type':'param_nav'}],
			},
		},
		1:{
			'common':{
				91:[700,{}],
				92:[710,{}],
				93:[706,{}],
				94:[107,{}],
				130:[1105,{}],
				131:[1106,{}],
			},
		},
		2:{
			'common':{
				91:[701,{}],
				92:[711,{}],
				94:[107,{}],
			},
			102:{
				80:[380,{}],
				81:[381,{}],
			},
		},
		3:{
			'common':{},
		},
	})

	# Add encoders to display
	for _ in range(200,208):
		self.default_layout['all'][0]['common'].update({_:[_,{}]})

	# Add menus to layouts
	for _ in range(401,403):
		self.default_layout['all'][1]['common'].update({_-321:[_,{}]})
	for _ in range(420,422):
		self.default_layout['all'][3]['common'].update({_-340:[_,{}]})
	
	# Add fader buttons
	#for _ in range(300,308):
		#self.default_layout['all'][0]['common'].update({_-220:[_,{}]})
	
	# Add Plugins action buttons
	for _ in range(32):
		self.default_layout['all'][0][102].update({_	:[_+260,{}]})
	
	# Add Plugins selection buttons
	
	for _ in range(16):
		self.default_layout['all'][0][102].update({_+48:[_+360,{}]})
	
def pre_midi(self,msg):
	
	## Unifies first 3 buttons on the top left to msg 0 to 2 because they follow the 8 buttons on the right.
	if msg.type in['note_on','note_off'] and msg.channel == 0:
		if msg.note in range(8,16):
			msg.note = 53
		elif msg.note in range(16,24):
			msg.note = 54
		elif msg.note in range(8):
			msg.note = 55
	
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
	'cc':{
		(60,0):[251,{'model':'r2'}],
	},
	'nt':{
		### Don't modify 53 and 54 since they're the layouts buttons
		(49,9):[923,[]],
		(50,9):[922,[]],
		(51,9):[921,[]],
		
		(98,0):[130,[]],
		(99,0):[131,[]],
		(84,0):[132,[]],
		
		# (110121) First 12 pads
		(36,9):[110,[]],
		(37,9):[111,[]],
		(38,9):[112,[]],
		(39,9):[113,[]],
		(40,9):[114,[]],
		(41,9):[115,[]],
		(42,9):[116,[]],
		(43,9):[117,[]],
		(44,9):[118,[]],
		(45,9):[119,[]],
		(46,9):[120,[]],
		(47,9):[121,[]],
		(48,9):[122,[]],
		
		# (70-79) 8 buttons on the top, from left to right, starting on the third one, beside layout 2.
		(53,0):[70,[]],
		(54,0):[71,[]],
		(55,0):[72,[]],
		(56,0):[73,[]],
		(57,0):[74,[]],
		(74,0):[75,[]],
		(87,0):[76,[]],
		(88,0):[77,[]],
		(89,0):[78,[]],
		(81,0):[79,[]],
		
		# (91-96) Transport buttons, from left to right.
		(91,0):[91,[]],
		(92,0):[92,[]],
		(93,0):[93,[]],
		(94,0):[94,[]],
		(95,0):[95,[]],
		(96,0):[96,[]],

		# 80-88) 8 buttons on the right, from left to right
		(24,0):[80,[]],
		(25,0):[81,[]],
		(26,0):[82,[]],
		(27,0):[83,[]],
		(28,0):[84,[]],
		(29,0):[85,[]],
		(30,0):[86,[]],
		(31,0):[87,[]],
		(51,0):[88,[]],

	},
	'pw':{},
}

for _ in range(200,208):
	# faders
	going_out['pw'].update({(_-200):[_,{'model':'p1','pickup':{'grab_zone':2,'tolerance':4}}]})

getting_in = {
	
	70:[{'model':'sy'},96],
	71:[{'model':'sy'},97],
	72:[{'model':'sy'},98],
	73:[{'model':'sy'},99],
	74:[{'model':'sy'},100],
	75:[{'model':'sy'},101],
	76:[{'model':'sy'},102],
	77:[{'model':'sy'},103],
	78:[{'model':'sy'},104],
	79:[{'model':'sy'},105],

	80:[{'model':'sy'},34],
	81:[{'model':'sy'},35],
	82:[{'model':'sy'},36],
	83:[{'model':'sy'},37],
	84:[{'model':'sy'},38],
	85:[{'model':'sy'},39],
	86:[{'model':'sy'},40],
	87:[{'model':'sy'},41],
	
	91:[{'model':'sy'},106],
	92:[{'model':'sy'},107],
	93:[{'model':'sy'},108],
	94:[{'model':'sy'},109],
	95:[{'model':'sy'},110],
	96:[{'model':'sy'},111],
	
	103:[{'model':'sy'},104],
}

data = {
	'name' : "Arturia KeyLab Mk2",
	'ports':['MIDIIN2 (KeyLab mkII 61)','MIDIOUT2 (KeyLab mkII 61)','startswith'],
	'fre_count':16,
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
			'tr_session_record_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_session_record_off':[8,[0,32,107,127,66,2,0,16,0,40]],
			'tr_readwrite_on':[8,[0,32,107,127,66,2,0,16,0,127]],
			'tr_readwrite_off':[8,[0,32,107,127,66,2,0,16,0,40]],

			},
}