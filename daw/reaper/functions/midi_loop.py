from mido import Message as MidiMsg

def midi_loop(self):
	""" Reaper's Midi Feedback. """

	for msg in self.routing.inport:

		if msg.type in['note_on','note_off']:
			for m in self.online['control']:
				m.midi_in_dispatch(msg)