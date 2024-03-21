import tkinter as tk
from tkinter import ttk

def speak(to_speak):
    # Implement this function to speak using a text-to-speech library of your choice
    # You can use accessible_output2 or another library for this purpose
    pass

class QuestionnaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Questionnaire")
        self.current_question = None
        self.answers = {}

        self.model_questions = {
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

        self.out_questions = {
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

        self.event_questions = {
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

        self.question_label = ttk.Label(self.root, text="", font=("Helvetica", 14))
        self.question_label.pack(pady=20)

        self.choice_buttons = []
        self.choices_var = tk.StringVar()
        for i in range(1, 5):  # Assuming a maximum of 4 choices
            choice = ttk.Radiobutton(self.root, text="", variable=self.choices_var, value="", command=self.answer_question)
            self.choice_buttons.append(choice)
            choice.pack(pady=10)

        self.current_question_key = None
        self.start_questionnaire(self.model_questions, 'model')

    def start_questionnaire(self, questions, question_key):
        self.current_question_key = question_key
        question = questions[question_key]
        self.question_label.config(text=f"Question: {question['text']}")
        choices = question.get('choices', {})
        for i, (choice_key, choice) in enumerate(choices.items()):
            if i < len(self.choice_buttons):
                self.choice_buttons[i].config(text=choice['text'], value=choice_key)
            else:
                break
        for i in range(len(choices), len(self.choice_buttons)):
            self.choice_buttons[i].config(text="", value="")

    def answer_question(self):
        question_key = self.current_question_key
        choice = self.choices_var.get()
        if question_key:
            self.answers[question_key] = choice

        next_question_key = self.answers[question_key]
        if next_question_key in self.event_questions:
            self.start_questionnaire(self.event_questions, next_question_key)
        elif next_question_key in self.out_questions:
            self.start_questionnaire(self.out_questions, next_question_key)
        else:
            # End of questionnaire, you can print or process the answers here
            print("Answers:", self.answers)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionnaireApp(root)
    root.mainloop()