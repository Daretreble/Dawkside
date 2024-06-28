from functions.speak import speak

def send_recv_select(self,control,*args,**kwargs):
	""" Send receive selection. """
	
	daw = self.daw
	main = daw.main
	modif = main.modif

	id = args[0]
	if modif('test',[911]):
		output = "sends" if id == 120 else "receives"
		speak("Utilize the initial six faders and encoders as "+output+".")
	else:
		sr = ['send','recv']
		sr_sel = sr[id-120]
		control.daw_vars['sendrecv']['selected'] = sr_sel
		control.settings[daw.short_name]['sendrecv']['selected'] = sr_sel
		speak(f"{self.send_recv_output[sr_sel]} selected")
		self.refresh(control,action='unit')