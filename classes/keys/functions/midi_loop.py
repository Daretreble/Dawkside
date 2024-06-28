from mido import Message as MidiMsg
from functions.misc import number_to_note
from functions.speak import speak

def midi_loop(self):
	""" Keys midi loop """

	main = self.main
	modif = main.modif

	for msg in self.port.inport:

		routing_destination = self.routing_destination
		passed = True

		if self.act and self.routing_destination:

			if self.pre_midi:
				self.pre_midi[0](self,msg)
				passed = self.pre_midi[1]
		
			if passed:
			
				event_type = msg.type
				key_passed = True
				cc_passed = True
				
				if msg.channel == 0:
				
					if event_type == 'pitchwheel':
						self.routing_destination.midiout(msg)
					
					if event_type in['note_on','note_off']:
					
						note = msg.note
						velo = msg.velocity
						bk = [1,3,6,8,10]
						ntpos = note % 12
						
						if event_type == 'note_on':
							if note not in self.notes_on:
								self.notes_on.append(note)
						else:
							if note in self.notes_on:
								self.notes_on.remove(note)
						
						for tmp in self.zones_config:
							if tmp[0]:
								if note in range(tmp[1],tmp[2]+1):
									note_tmp = note+(tmp[3]*12)
									if note_tmp in range(128):
										
										# Velocity curve
										if self.velo_curve:
											if event_type == 'note_on' and note % 12 not in bk:
												velotmp = round(velo + (velo*self.velo_curve))
												velo = velotmp if velotmp in range(0,128) else 127
										
										if self.routing_destination:
											if key_passed:
												self.routing_destination.midiout(MidiMsg(event_type,note=note_tmp,channel=tmp[4],velocity=velo))
											if msg.type == 'note_on':
												
												# Note info with modif help
												if modif('test',[911]):
													speak(number_to_note(note_tmp)[0].replace('#',' Sharp'))
												
												# Split keyboard with modif Add
												if modif('test',[910]):
													self.zone_manage(note,action='split')
										
										

					if event_type == 'control_change':
						
						control = msg.control
						value = msg.value
						
						if msg.channel == 15:
						
							msg.channel = 14
							lpcc_out.send(msg)
						
						if msg.channel == 0:
							
							if control == 1:
								#self.modwheel[3] = msg.value
								cc_passed = False
								#if self.modwheel[0]:
									#client.send_message(f"/fxparam/{self.modwheel[0]}/value",ptchCnv('c2v',msg.value,self.modwheel[1],self.modwheel[2]))
						
							if control == 64:
								for tmp in self.zones_config:
									cc_passed = False
									if tmp[0] and tmp[5]:
										self.routing_destination.midiout(MidiMsg(event_type,control=64,channel=tmp[4],value=value))
						
						if cc_passed:
							self.routing_destination.midiout(msg)