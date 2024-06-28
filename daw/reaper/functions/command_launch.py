def command_launch(self,control,id,info,options):
	""" Reaper's Command actions. """

	main = self.main
	modif = main.modif
	state = info[1]
	mode = control.daw_vars['mode']

	## Undo
	if state and id == 80:
		if modif('test',[900]):
			self.client.send_message('/action',40030)
		else:
			self.client.send_message('/action',40029)

	## Redo
	if state and id == 81:
		self.client.send_message('/action',40030)

	## Tap tempo
	if state and id == 104:
		self.client.send_message('/action',1134)

	## Go to previous track
	if state and id == 105:
		self.client.send_message('/action',40286)

	## Go to next track
	if state and id == 106:
		self.client.send_message('/action',40285)

	## Insert captured MIDI data
	if state and id == 107:
		self.client.send_message('/action',40686)