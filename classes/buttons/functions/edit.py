import os
import pyautogui
import json
import pprint
from functions.misc import dict_test
from functions.questionnaire import questionnaire
from functions.testers import *
from functions.speak import speak

def edit(self,**kwargs):
	""" Edits buttons. """

	control = self.control
	daw = self.control.daw
	main = daw.main
	plugins = daw.plugins
	user = plugins.user

	main.safety_guards['question_access'][0] = True

	passed = True

	button_type = kwargs['button_type']
	pos = kwargs['pos']
	if 'disp' in kwargs:
		disp = kwargs['disp']
	
	where_to_save = {}
	to_save = {}
	add_replace = 'replace'

	model_questions = {
		'model':{
			'text':"What type of action for that button?",
			'choices':{
				'command':{
					'text':"default command action",
				},
				'pressed':{
					'text':"on press",
				},
				'released':{
					'text':"on release",
				},
			}
		},
	}
	
	add_replace_questions = {
			'add_replace':{
				'text':"The button already exists. What do you want to do with it?",
				'choices':{
					'add':{
						'text':"Add to actual sequence",
					},
					'replace':{
						'text':"Replace",
					},
				}
			}
		}
	
	time_out_questions = {
			'time_out':{
				'text':"Add a time out in milliseconds, if needed.",
				'default':None,
				'format':int,
			}
		}
		
	event_type_questions = {
		'event_type':{
			'text':"What type of event to send for that button?",
			'choices':{
				'command':{
					'text':"Command",
				},
				'plugin_param':{
					'text':"Plugin parameter",
				},
				'midi_cc':{
					'text':"Midi Control change",
				},
				'midi_note':{
					'text':"Midi Note",
				},
				'sysex':{
					'text':"Sysex data",
				},
				'osc':{
					'text':"OSC Message",
				},
				'mouse':{
					'text':"Mouse event",
				},
				'app':{
					'text':"Application launch",
				},
			}
		},
	}
	
	event_questions = {
		# Command
		'command':{
			'id':{
				'text':"What is the command id?",
				'tester':[command_check,False],
				'format':int,
			},
			'params':{
				'text':"What is the parameter dictionnary to send, if any? (refer to the documentation)",
				'default':None,
				'tester':[json_check,False],
			},
		},
		# Plugin parameter
		'plugin_param':{
			'param_id':{
				'text':"What is the parameter id?",
				'default':plugins.last_param['num'] if plugins.last_param['act'] else 1,
				'tester':[param_check,[plugins.params]],
				'format':int,
			},
			'value':{
				'text':"What is the value to send?",
				'default':'1.0',
				'tester':[normalized_check,False],
				'format':float,
			},
		},
		# Midi CC
		'midi_cc':{
			'control':{
				'text':"What is the control change number to send? (from 0 to 127)",
				'default':64,
				'tester':[seven_bit_check,False],
				'format':int,
			},
			'value':{
				'text':"What is the value to send? (from 0 to 127)",
				'default':127,
				'tester':[seven_bit_check,False],
				'format':int,
			},
			'channel':{
				'text':"On which channel? (from 0 to 15)",
				'default':0,
				'tester':[four_bit_check,False],
				'format':int,
			},
		},
		# Midi Note
		'midi_note':{
			'note':{
				'text':"What is the note number number to send? (from 0 to 127)",
				'default':64,
				'tester':[seven_bit_check,False],
				'format':int,
			},
			'velocity':{
				'text':"What is the velocity to send? (from 0 to 127 or Enter to skip and use pad's velocity)",
				'default':False,
				'tester':[seven_bit_check,False],
				'format':int,
			},
			'channel':{
				'text':"On which channel? (from 0 to 15)",
				'default':0,
				'tester':[four_bit_check,False],
				'format':int,
			},
		},
		# Sysex
		'sysex':{
			'data':{
				'text':"Enter a series of decimal numbers, separated by a comma.",
				'tester':[sysex_check,False],
				'format':tuple,
			},
		},
		# OSC
		'osc':{
			'message':{
				'text':"What's the OSC message number to send?"
			},
			'arguments':{
				'text':"What are the arguments to send?",
				'format':'osc_args',
			},
		},
		# Mouse event
		'mouse':{
			'event':{
				'text':"What should the mouse do?",
				'choices':{
					'move':{
						'text':"Move to the actual position. Don't forget to move the mouse pointer where needed",
						'content':[pyautogui.position()[0],pyautogui.position()[1]],
					},
					'left_click':{
						'text':"Left click",
					},
					'right_click':{
						'text':"Right click",
					},
					'double_click':{
						'text':"Double click",
					},
				}
			}
		},
		# Application launch
		'app':{
			'name':{
				'text':"What's that application full name, with extension?"
			},
			'arguments':{
				'text':"What are the arguments to send?",
			},
		},
	}

	if button_type == 'user':
		
		del(event_type_questions['event_type']['choices']['plugin_param'])

		where_questions = {
			'affected_daw':{
				'text':"Which daw is affected by that button?",
				'choices':{
					'all':{
						'text':"All active daws at once.",
					},
					'selected':{
						'text':"The selected daw",
					},
				}
			},
			'reach':{
				'text':"What's that button reach?",
				'choices':{
					'permanent':{
						'text':"Permanent. The button is present in every context",
					},
					'common':{
						'text':"Common. The button is common to all modes",
					},
					'mode':{
						'text':"Mode. The button is dependant on the selected mode",
					},
				}
			},
		}
		for key,value in main.daws.items():
			where_questions['affected_daw']['choices'][value.short_name] = {'text':value.name}
		
		if passed:
			if questionnaire(where_questions,where_to_save) == 'exit':
				passed = False
		if passed:
			if questionnaire(model_questions,where_to_save) == 'exit':
				passed = False
		
		if passed:
			reach = where_to_save['reach']
			affected_daw = where_to_save['affected_daw']
			dest_layout = control.layouts[affected_daw if affected_daw not in ['all','selected'] else 'all']
			present_in = {
				'permanent':dict_test(dest_layout,['permanent',pos,where_to_save['model']]),
				'common':dict_test(dest_layout,[disp,'common',pos,where_to_save['model']]),
				'mode':dict_test(dest_layout,[disp,control.daw_vars['mode'],pos,where_to_save['model']]),
		}
		
	if passed and button_type == 'plugin_button':
		
		if passed:
			if questionnaire(model_questions,where_to_save) == 'exit':
				passed = False

	if passed and (where_to_save['model'] != 'command' and ( (button_type == 'user' and present_in[reach]) or (button_type == 'plugin_button' and dict_test(plugins.user_params,[plugins.name,plugins.page[0],button_type,pos,where_to_save['model'] ])) ) ):

		add_replace = {}
		if passed:
			if questionnaire(add_replace_questions,add_replace) == 'exit':
				passed = False
			else:
				add_replace = add_replace['add_replace']
		
		if add_replace == 'add':
			if passed:
				if questionnaire(time_out_questions,to_save) == 'exit':
					passed = False
		
	if passed:
		if where_to_save['model'] == 'command':
			to_save['event_type'] = 'command'
		else:
			if passed:
				if questionnaire(event_type_questions,to_save) == 'exit':
					passed = False
		if passed:
			if questionnaire(event_questions[to_save['event_type']],to_save) == 'exit':
				passed = False

	if passed and button_type == 'plugin_button':

		if not plugins.user.is_saved('page'):
			plugins.user.page_create()			
		dest_tmp = plugins.user_params[plugins.name][plugins.page[0]][button_type]
	
	if passed and button_type == 'user':
		
		for key,value in present_in.items():
			if key != reach:
				if value:
					pass
					
			else:
				# Adds permanent
				if key == 'permanent':
					if 'permanent' not in dest_layout:
						dest_layout['permanent'] = {}
					dest_tmp = dest_layout['permanent']
				
				# Adds common
				if key == 'common':
					if disp not in dest_layout:
						dest_layout[disp] = {}
					if 'common' not in dest_layout[disp]:
						dest_layout[disp]['common'] = {}
					dest_tmp = dest_layout[disp]['common']
				
				# Adds mode
				if key == 'mode':
					if disp not in dest_layout:
						dest_layout[disp] = {}
					if control.daw_vars['mode'] not in dest_layout[disp]:
						dest_layout[disp][control.daw_vars['mode']] = {}
					dest_tmp = dest_layout[disp][control.daw_vars['mode']]

	if passed:
		if add_replace == 'add':
			if where_to_save['model'] in dest_tmp[pos]:
				dest_tmp[pos][where_to_save['model']].append(to_save)
			else:
				dest_tmp[pos][where_to_save['model']] = to_save	
		else:
			if where_to_save['model'] == 'command':
				dest_tmp[pos] = [to_save['id'],{} if 'params' not in to_save else json.loads(to_save['params'])]
			else:
				if pos not in dest_tmp:
					dest_tmp[pos] = {}
				if isinstance(dest_tmp[pos],list):
					dest_tmp[pos] = {
						where_to_save['model']:{
							'event_type':'command',
							'id':dest_tmp[pos][0],
							'params':dest_tmp[pos][1],
						}
					}
				dest_tmp[pos].update({where_to_save['model']:[to_save]})
			
		#### DEV Very rough temporary latch setting. Make it better with edit functions later.
		# check latches
		if 'pressed' in dest_tmp[pos] and 'released' in dest_tmp[pos]:
			latch_question = {
				'latch':{
					'text':"Both pressed and released states are present for that button. Do you want to make it latch, if applicable?",
					'choices':{
						True:{
							'text':"Yes",
						},
						False:{
							'text':"No",
						},
					}
				}
			}
			latch = {}
			if questionnaire(latch_question,latch) == 'exit':
				passed = False
			else:
				if latch['latch']:
					if 'options' not in dest_tmp[pos]:
						dest_tmp[pos]['options'] = {'latch':{'state':True}}
					elif 'latch' in dest_tmp[pos]['options']:
						dest_tmp[pos]['options']['latch']['state'] = True
					else:
						dest_tmp[pos]['options'] = {'latch':{'state':True}}

	

		if passed:
			if button_type == 'plugin_button':
				user.param_save()
				daw.pVar = ['trackreload']
			
			if button_type == 'user':
				control.layout_save()
				control.layout_prepare(control.layout_active)

	main.safety_guards['question_access'][0] = False
	os.system('cls')
	speak("Questionnaire completed successfully." if passed else "Exiting the questionnaire.", printout=True)