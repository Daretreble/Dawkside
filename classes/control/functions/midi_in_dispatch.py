def midi_in_dispatch(self,msg):
	""" Manages daw's midi in to control devices. """

	if self.daw_vars['mode'] in [130,131]:
		self.modes.sections[self.daw_vars['mode']]['class'].midi_in(True if msg.type == 'note_on' else False,msg.note)