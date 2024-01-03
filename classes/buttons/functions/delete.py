import os
from functions.misc import dict_test
from functions.questionnaire import questionnaire
from functions.speak import speak

def delete(self,**kwargs):
	""" Deletes buttons. """

	control = self.control
	daw = self.control.daw
	main = daw.main
	plugins = daw.plugins
	user = plugins.user

	button_type = kwargs['button_type']
	pos = kwargs['pos']
	if 'disp' in kwargs:
		disp = kwargs['disp']
	
	if button_type == 'plugin_button':
		if user.is_saved('page') and pos in plugins.user_params[plugins.name][plugins.page[0]][button_type]:
			del(plugins.user_params[plugins.name][plugins.page[0]][button_type][pos])
			user.param_save()
			daw.pVar = ['fxreload']
			speak(f"Button {pos+1} deleted on page {plugins.page[0]}")
		else:
			speak("No plugin button to delete")

	if button_type == 'user':

		answers = {}
		for dest in['all','reaper']:
			
			dest_layout = control.layouts[dest]
			present_in = {
				'mode':dict_test(dest_layout,[disp,control.daw_vars['mode'],pos]),
				'common':dict_test(dest_layout,[disp,'common',pos]),
				'permanent':dict_test(dest_layout,['permanent',pos]),
			}
			delete_questions = {}
			answers[dest] = {}
			for key,value in present_in.items():
				if value:
					delete_questions.update({
						key:{
							'text':f"Do you want to delete on {dest} for {key}?",
							'choices':{
								True:{
									'text':"Yes",
								},
								False:{
									'text':"No",
								},
							}
						}
					})
			questionnaire(delete_questions,answers[dest])
		os.system('cls')
		for d in answers:
			for key,value in answers[d].items():
				if value:
					if key == 'permanent':
						del(control.layouts[d]['permanent'][pos])
					if key == 'common':
						del(control.layouts[d][disp]['common'][pos])
					if key == 'mode':
						del(control.layouts[d][disp][control.daw_vars['mode']][pos])
						
		control.layout_save()
		control.layout_prepare(control.layout_active)
		speak(f"Button number {pos} deleted on page {disp+1}")