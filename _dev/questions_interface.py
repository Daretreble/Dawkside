import accessible_output2.outputs.auto
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

accessOut = accessible_output2.outputs.auto.Auto()

def speak(to_speak):
	accessOut.speak(str(to_speak), interrupt=True)

model_questions = {
	'model': {
		'text': "What type of action for that button?",
		'choices': {
			'1': {
				'text': "Fixed",
			},
			'2': {
				'text': "Latch",
			},
			'3': {
				'text': "Momentary",
			},
		}
	},
}

out_questions = {
	'out': {
		'text': "What type of event to send for that button?",
		'choices': {
			'99': {
				'text': "Command",
			},
			'1': {
				'text': "Plugin parameter",
			},
			'2': {
				'text': "Midi Control change",
			},
			'3': {
				'text': "Midi Note",
			},
			'4': {
				'text': "OSC Message",
			},
			'5': {
				'text': "Mouse event",
			},
		}
	},
}

event_questions = {
	# Command
	'99': {
		'command_id': {
			'text': "What is the command id?",
		},
		'params': {
			'text': "What is the parameter to send?",
		},
	},
	# Plugin parameter
	'1': {
		'param_id': {
			'text': "What is the parameter id?",
		},
		'min': {
			'text': "What's the minimum value, from 0.0 to 1.0?",
		},
		'max': {
			'text': "What's the maximum value, from 0.0 to 1.0?",
		},
		'on': {
			'text': "What's the on value, from 0.0 to 1.0?",
		},
	},
	# Midi CC
	'2': {
		'cc_on': {
			'text': "What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on': {
			'text': "What's the value to send on press, from 1 to 16?",
		},
	},
	# Midi Note
	'3': {
		'cc_on': {
			'text': "What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on': {
			'text': "What's the value to send on press, from 1 to 16?",
		},
	},
	# OSC
	'4': {
		'cc_on': {
			'text': "What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on': {
			'text': "What's the value to send on press, from 1 to 16?",
		},
	},
	# Mouse event
	'5': {
		'cc_on': {
			'text': "What's the control change number to send on press? (from 0 to 127)"
		},
		'value_on': {
			'text': "What's the value to send on press, from 1 to 16?",
		},
	},
}

button_type = 'user'
to_save = {}

def questionnaire(to_ask, dest):
	for model, question in to_ask.items():
		root = tk.Tk()
		root.title("Questionnaire")

		def save_answer():
			answer = entry.get()
			if 'choices' in question and answer not in question['choices']:
				messagebox.showerror("Invalid Choice", "Please enter a valid choice.")
			else:
				if dest:
					to_save[dest][model] = answer
				else:
					to_save[model] = answer
				root.destroy()

		question_label = tk.Label(root, text=f"Question. {question['text']}")
		question_label.pack()

		if 'choices' in question:
			for answer, choice in question['choices'].items():
				radio = tk.Radiobutton(root, text=choice['text'], value=answer)
				radio.pack()

		entry = tk.Entry(root)
		entry.pack()

		submit_button = tk.Button(root, text="Submit", command=save_answer)
		submit_button.pack()

		root.mainloop()

	# os.system('cls')

questionnaire(model_questions, False)
to_save['in'] = {}
questionnaire(out_questions, 'in')
questionnaire(event_questions[to_save['in']['out']], 'in')
if to_save['model'] in ['2', '3']:
	to_save.update({'out': {}})
	questionnaire(out_questions, 'out')
	questionnaire(event_questions[to_save['out']['out']], 'out')

speak("Questionnaire completed")