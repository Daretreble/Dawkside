import time
from mido import Message as MidiMsg
from functions.misc import pitch_convert

def fre_feedback(self,*args):
	""" Send midi feedback back to control surface. """
	
	outmode = args[0]
	pos = args[1]
	value = max(0.0, min(args[2] if args[2] else 0.0, 1.0))
	daw = self.daw

	if self.daw_vars['outmode'] == outmode:

		if time.time()-self.switchtime > 0.1:
			fstmp = self.fader_state[pos]
			input_value = pitch_convert('v2c',value)
			fstmp[2] = input_value
			if fstmp[0]:
				if fstmp[1] != fstmp[2]:
					fstmp[0] = False
	
		if self.getting_in and pos+200 in self.getting_in:
			getting_in = self.getting_in[pos+200]
			model = getting_in[0]['model']
			
			if model == 'cc':
				msg = MidiMsg(
					'control_change',
					channel=getting_in[2],
					control=getting_in[1],
					value=pitch_convert('v2c',value)
				)
				self.port.midiout(msg)
			
			if model == 'p1':
				
				msg = MidiMsg(
					'pitchwheel',
					channel=getting_in[1],
					pitch=pitch_convert('v2p1',value)
				)
				self.port.midiout(msg)