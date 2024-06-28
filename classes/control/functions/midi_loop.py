from functions.speak import speak

def midi_loop(self):
	""" Midi loop for control surfaces. """

	print_midi = True if '--show-midi' in self.main.queries else False
	
	for msg in self.port.inport:

		if print_midi:
			print(self.name,msg)
			#speak(str(msg))
	
		if self.pre_midi:
				self.pre_midi[0](self,msg)
				passed = self.pre_midi[1]
		
		if self.routing_destination:

			self.routing_destination.midiout(msg)
		
		else:
		
			passed = True
			event_type = msg.type
			
			if passed:
			
				if event_type in['note_on','note_off']:
				
					note = msg.note
					velo = msg.velocity
					
					# toggle type
					tt = self.toggle_type
					if tt:
						if tt == 1:
							state = False if event_type == 'note_off' else True
							velo = 127 if state else 0
					else:
						state = False if velo == 0 else True
					
					if (note,msg.channel) in self.going_out['nt']:
						self.matrix_send([self.going_out['nt'][(note,msg.channel)],state,velo])
					
				if event_type == 'pitchwheel':
				
					pitch = msg.pitch
					channel = msg.channel
					state = True
					
					if (channel) in self.going_out['pw']:
						self.matrix_send([self.going_out['pw'][(channel)],state,pitch])
				
				if event_type == 'control_change':
				
					control = msg.control
					value = msg.value
					state = False if value == 0 else True
					
					if (control,msg.channel) in self.going_out['cc']:
						self.matrix_send([self.going_out['cc'][(control,msg.channel)],state,value])


			if self.post_midi:
				self.post_midi[0](self,msg)
				