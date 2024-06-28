# Arturia KeyLab Mk2 Setup

from mido import Message as MidiMsg

def control_init(self):

	# Generate displays
	self.displays_override = {}
	for daws in self.main.daws:

		self.displays_override.update({
			daws.short_name:{}
		})

		disp_over = self.displays_override[daws.short_name]
		
		disp_over.update({
			'permanent':{
				133:[1,911,{}],
			},
			0:{
				'common':{
					100:[1,98,{}],
					99:[1,80,{}],
					91:[1,95,{}],
					90:[1,94,{}],
				},
				100:{},
				101:{
					56:[1,120,{}],
					57:[1,121,{}],
				},
				102:{
					40:[1,380,{}],
					41:[1,381,{}],
					122:[1,376,{}],
					123:[1,377,{}],
					120:[1,378,{}],
					121:[1,379,{}],
				},
				130:{},
				131:{},
				132:{},
			},
			1:{
				'common':{
					99:[1,81,{}],
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
			disp_over[0]['common'].update({_:[1,_,{}]})

		# Add menus to displays
		for _ in range(400,400+len(daws.modes)):
			disp_over[0]['common'].update({_-330:[1,_,{}]})
		for _ in range(410,410+len(self.main.outmodes)):
			disp_over[1]['common'].update({_-340:[1,_,{}]})
		for _ in range(430,430+len(self.modes.sections)):
			disp_over[2]['common'].update({_-360:[1,_,{}]})
		for _ in range(420,420+len(self.main.daws)):
			disp_over[3]['common'].update({_-350:[1,_,{}]})
		
		# Add fader buttons
		for _ in range(300,308):
			disp_over[0]['common'].update({_-220:[1,_,{}]})
		
		# Add Plugins selection buttons
		count = 360
		for r in[56,48]:
			for c in range(8):
				disp_over[0][102].update({c+r:[1,count,{}]})
				count+=1
		
		# Add modes matrix
		for i in self.modes.sections:
			for j in range(64):
				disp_over[0][i].update({j:[1,j+800,{}]})

going_out = {
	'cc':{
		### Don't modify 48 and 49 since they're the displays buttons
		(48,0):[921,[]],
		(49,0):[922,[]],
	},
	'nt':{},
	'pw':{},
}

getting_in = {}
"""
# (0-63) Add 64 pads
for _ in range(64):
	going_out['nt'].update({(_+36,0):[_,[]]})
	getting_in.update({_:[{'model':'nt'},_+36]})

# (70-77) Add the 8 buttons located directly over the 64 pads.
for _ in range(70,78):
	going_out['cc'].update({(_+32,0):[_,[]]})
	getting_in.update({_:[{'model':'cc'},_+32]})

# (80-87) Add the 8 buttons at the top of the middle section
for _ in range(80,88):
	going_out['cc'].update({(_-60,0):[_,[]]})
	going_out['nt'].update({(_-80,0):[_,[]]})
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
	[151,116],




]
for _ in cc_btns:
	going_out['cc'].update({(_[1],0):[_[0],[]]})
	getting_in.update({ _[0]:[{'model':'cc'},_[1]],  })

# (200,207) First 8 faders
for _ in range(200,208):
	going_out['cc'].update({(_-129,0):[_,{'model':'r1'}]})
"""
data = {
	'name' : "Ableton Push 1",
	'short_name':"apush1",
	'types':{
		'control':{
			'ports':['MIDIIN2 (KeyLab mkII 61)','MIDIOUT2 (KeyLab mkII 61)'],
			'preferred_daw':'reaper',
			'mode':102,
			'outmode':12,
			'matrixin':getting_in,
			'matrixout':going_out,
			'control_init':[control_init],
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
			}
		},
		'keys':{
			'ports' : ['KeyLab mkII','KeyLab mkII'],
		},
	}
