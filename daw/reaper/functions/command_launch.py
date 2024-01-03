def command_launch(self,control,id,info,options):
	""" Reaper's Command actions. """

	main = self.main
	modif = main.modif
	state = info[1]
	mode = control.daw_vars['mode']

	## Undo
	if id == 80 and state:
		self.client.send_message('/action',40029)

	## Redo
	if id == 81 and state:
		self.client.send_message('/action',40030)