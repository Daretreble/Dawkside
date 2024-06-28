import time
from functions.misc import model_convert,value_from_normalized
from functions.misc import pitch_convert
from functions.speak import speak

def fre_process(self,info):
	""" Processes faders, rotaries and encoders data. """

	daw = self.daw
	main = daw.main
	modif = main.modif
	sn = daw.short_name
	value = info[2]
	pos = (info[0][0]-200)+(8*(self.daw_vars['rotary_group']-1))
	if pos != self.last_touched[0] or not self.last_touched[0] or time.time() - self.last_touched[1] > 5:
		new_fader_action = True
		self.last_touched[0] = pos
		self.last_touched[1] = time.time()
	else:
		new_fader_action = False

	opt = info[0][1]
	model = opt['model']
	pickup = True if 'pickup' in opt else False
	osc_msg = False
	value_string = ''
	fre_tmp = False
	
	# Selected Track (volume, pan and sends/return
	if self.daw_vars['outmode'] == 11:
		tmp = daw.fre['track']
		
		if pos < 6:
			if pos in tmp[self.daw_vars['sendrecv']['selected']]:
				sr_sel = self.daw_vars['sendrecv']['selected']
				
				if sr_sel == 'send':

					# Send messages
					if sn == 'reaper':
						osc_msg = f"/track/send/{pos+1}/volume"
					if sn == 'live':
						osc_msg = f"/live/track/set/send"
				
				if sr_sel == 'recv':

					# Send messages
					if sn == 'reaper':
						osc_msg = f"/track/recv/{pos+1}/volume"
				
				fre_tmp = tmp[self.daw_vars['sendrecv']['selected']][pos]
				value_string = fre_tmp['valstr']
		if pos in [6,7] and pos in tmp['track']:
			if pos == 6:
				
				# Pan message
				if sn == 'reaper':
					osc_msg = "/track/pan"
				if sn == 'live':
					osc_msg = "/live/track/set/panning"
			
			if pos == 7:

				# Volume message
				if sn == 'reaper':
					osc_msg = "/track/volume"
				if sn == 'live':
					osc_msg = "/live/track/set/volume"

			fre_tmp = tmp['track'][pos]
			value_string = fre_tmp['valstr']
			
	# Set selected plugin parameter
	if self.daw_vars['outmode'] == 12:
		tmp = daw.fre['plugins']['faders']
		if pos in tmp:
			
			# Plugins parameters message
			if sn == 'reaper':
				osc_msg = f"/fxparam/{tmp[pos]['prm']}/value"
			if sn == 'live':
				osc_msg = "/live/device/set/parameter/value"
			
			fre_tmp = tmp[pos]
			value_string = daw.plugins.params[tmp[pos]['prm']]['valstr']
	
	if self.faders_speak[0] and new_fader_action or modif('test',[911]):
		if fre_tmp:
			speak(fre_tmp['name'],repeat=False)
		else:
			speak("Empty")
	
	tolerated = True
	if pickup and not modif('test',[911]):
		fstmp = self.fader_state[pos]
		fre_value = pitch_convert('v2c',model_convert(model,value,value))
		fstmp[1] = fre_value
		self.switchtime = time.time()
		## Debug (working): if the beep is not triggered, remove the value range in that condition.
		if time.time() - self.fader_state[pos][4] > 1 and value not in range(fstmp[2]-opt['pickup']['grab_zone'],fstmp[2]+opt['pickup']['grab_zone']):
			fstmp[3] = 0
		else:
			fstmp[3] += 1
		tolerated = True if fstmp[3] >= opt['pickup']['tolerance'] else False
		if not fstmp[0]:
			if fstmp[1] in range(fstmp[2]-opt['pickup']['grab_zone'],fstmp[2]+opt['pickup']['grab_zone']):
				fstmp[0] = True
				fstmp[2] = fstmp[1]
				if tolerated:
					main.play_sound('tick')
			else:
				if time.time() - self.fader_state[pos][4] > 0.2:
					if tolerated:
						main.play_sound('high' if fstmp[1] < fstmp[2] else 'low')
					self.fader_state[pos][4] = time.time()
		
	if fre_tmp and not modif('test',[911]) and (not pickup or (pickup and fstmp[0])):
	
		new_value = model_convert(model,value,fre_tmp['pitch'][0])
		
		if sn == 'reaper':
			if tolerated and self.daw_vars['outmode'] == 11:
				for m in daw.online['control']:
					m.fre_feedback(11,pos,new_value)
		
		if sn == 'live':
			if tolerated and self.daw_vars['outmode'] == 11:
				if  pos < 6:
					self.daw.fre['track']['send'][pos]['valstr'] = daw.fake_valstr(pos,new_value)
					for m in daw.online['control']:
						m.fre_feedback(self.daw_vars['outmode'],pos,new_value)
				elif pos == 6:
					self.daw.fre['track']['track'][pos]['valstr'] = daw.fake_valstr(pos,new_value)
				elif pos == 7:
					self.daw.fre['track']['track'][pos]['valstr'] = daw.fake_valstr(pos,new_value)
		
		if new_value:
			fre_tmp['pitch'][0] = new_value
			
			if osc_msg and (fre_tmp['pitch'][0] != fre_tmp['pitch'][1]):
				
				fre_tmp['pitch'][1] = fre_tmp['pitch'][0]

				if time.time() - self.fader_state[pos][4] > 0.5:
					if tolerated:
						# Add to have the value string said while moving.
						pass
						#speak(value_string)
					self.fader_state[pos][4] = time.time()
				
				# Format values
				if sn == 'reaper':
					value_out = fre_tmp['pitch'][0]
				if sn == 'live':
					if self.daw_vars['outmode'] == 11:
						if pos < 6:
							value_out = (daw.track.index[0],pos,fre_tmp['pitch'][0])
						elif pos == 6:
							value_out = (daw.track.index[0],fre_tmp['pitch'][0]-0.5)
						elif pos == 7:
							value_out = (daw.track.index[0],fre_tmp['pitch'][0])
					if self.daw_vars['outmode'] == 12:
						min = fre_tmp['min']
						max = fre_tmp['max']
						value_tmp = fre_tmp['pitch'][0]
						converted_value = value_from_normalized(value_tmp,min,max)
						value_out = (daw.track.index[0],daw.plugins.index[0]-1,tmp[pos]['prm']-1,converted_value)

				if tolerated:
					daw.client.send_message(osc_msg,value_out)