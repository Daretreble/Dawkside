def refresh(self,*args,**kwargs):
	""" Refreshes track class buttons and fre's """
	
	daw = self.daw
	track = daw.fre['track']
	action = kwargs['action']
	
	if action == 'unit':
		controls = [args[0]]

	if action == 'full':
		controls = daw.online['control']
	
	for m in controls:

		sr_type = m.daw_vars['sendrecv']['selected']
		sr = ['send','recv']
		for _ in[120,121]:
			c = sr[_-120]+'_sel_on' if sr[_-120] == sr_type else sr[_-120]+'_sel_off'
			m.matrix_in(_,c,action='unit')
		
		# Refresh faders
		for _ in range(8):
			# Send and receive set
			if _ < 6:
				if _ in track[sr_type]:
					c = 'fre_'+sr_type+'_on'
					output_pitch = track[sr_type][_]['pitch'][0]
				else:
					c = 'fre_'+sr_type+'_off'
					output_pitch = 0
			# Volume and Pan set
			else:
				c = 'fre_volume' if _ == 7 else 'fre_pan'
				output_pitch = track['track'][_]['pitch'][0]
			if m.daw_vars['outmode'] == 11:
				m.matrix_in(_+300,c,action='unit')
			m.fre_feedback(11,_,output_pitch)