import accessible_output2.outputs.auto
accessOut = accessible_output2.outputs.auto.Auto()
import os
import pprint

def speak(to_speak):
	accessOut.speak(str(to_speak), interrupt=True)

model_questions = {
	'model':{
		'text':"What type of action for that button?",
		'choices':{
			'1':{
				'text':"Fixed",
			},
			'2':{
				'text':"Latch",
			},
			'3':{
				'text':"Momentary",
			},
		}
	},
}
out_questions = {
	'out':{
		'text':"What type of event to send for that button?",
		'choices':{
			'99':{
				'text':"Command",
			},
			'1':{
				'text':"Plugin parameter",
			},
			'2':{
				'text':"Midi Control change",
			},
			'3':{
				'text':"Midi Note",
			},
			'4':{
				'text':"OSC Message",
			},
			'5':{
				'text':"Mouse event",
			},
		}
	},
}
event_questions = {
	# Command
	'99':{
		'command_id':{
			'text':"What is the command id?",
			'default':1
		},
		'params':{
			'text':"What is the parameter to send?",
		},
	},
	# Plugin parameter
	'1':{
		'param_id':{
			'text':"What is the parameter id?",
		},
		'min':{
			'text':"What's the minimum value, from 0.0 to 1.0?",
		},
		'max':{
			'text':"What's the maximum value, from 0.0 to 1.0?",
		},
		'on':{
			'text':"What's the on value, from 0.0 to 1.0?",
		},
	},
	# Midi CC
	'2':{
		'cc_on':{
			'text':"What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on':{
			'text':"What's the value to send on press, from 1 to 16?",
		},
	},
	# Midi Note
	'3':{
		'cc_on':{
			'text':"What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on':{
			'text':"What's the value to send on press, from 1 to 16?",
		},
	},
	# OSC
	'4':{
		'cc_on':{
			'text':"What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on':{
			'text':"What's the value to send on press, from 1 to 16?",
		},
	},
	# Mouse event
	'5':{
		'cc_on':{
			'text':"What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on':{
			'text':"What's the value to send on press, from 1 to 16?",
		},
	},
}

button_type = 'user'
to_save = {}

def questionnaire(to_ask,dest):
	for model,question in to_ask.items():
		os.system('cls')
		quest_out = ""
		quest_out += f"Question. {question['text']}.\n"
		if 'choices' in question:
			for answer,choice in question['choices'].items():
				quest_out += f"Enter {answer} for {choice['text']}.\n"
		print(quest_out)
		speak(f"{quest_out} Your answer?")
		passed = False
		while not passed:
			tmp_result = input("Your Answer> ")
			if 'choices' in question:
				if tmp_result in question['choices']:
					passed = True
			else:
				if tmp_result != '':
					passed = True
			if passed:
				if dest:
					to_save[dest][model] = tmp_result
				else:
					to_save[model] = tmp_result
			else:
				os.system('cls')
				print(quest_out)
				tmp_result = "Skipping that question" if tmp_result == "" else tmp_result
				speak(f"{tmp_result} is not a valid choice. Let me repeat the question. {quest_out} Try again?")

	#os.system('cls')

questionnaire(model_questions,False)
to_save['in'] = {}
questionnaire(out_questions,'in')
questionnaire(event_questions[to_save['in']['out']],'in')
if to_save['model'] in['2','3']:
	to_save.update({'out':{}})
	questionnaire(out_questions,'out')
	questionnaire(event_questions[to_save['out']['out']],'out')

pprint.pprint(to_save)