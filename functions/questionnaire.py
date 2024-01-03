import os
import pprint
from functions.speak import speak
from functions.misc import convert_to_appropriate_type

def questionnaire(to_ask,dest,**kwargs):
	for model,question in to_ask.items():
		os.system('cls')
		quest_out = ""
		quest_out += f"Question. {question['text']}.\n"
		quest_count = 1
		answer_tmp = []
		choice_tmp = []
		if 'choices' in question:
			for answer,choice in question['choices'].items():
				if not kwargs or ('accepted_answers' in kwargs and answer in kwargs['accepted_answers']):
					quest_out += f"Enter {quest_count} for {choice['text']}.\n"
					answer_tmp.append(answer)
					if 'content' in choice:
						choice_tmp.append(choice['content'])
					else:
						choice_tmp.append(False)
						
					quest_count += 1
		print(quest_out)
		speak(f"{quest_out} Your answer?")
		passed = False
		while not passed:
			result_tmp = input("Your Answer> ")

			if result_tmp == 'exit':
				return 'exit'

			if 'choices' in question:
				if result_tmp != '' and result_tmp.isdigit() and int(result_tmp) in range(1,len(answer_tmp)+1):
					if choice_tmp[int(result_tmp)-1]:
						result_tmp = [answer_tmp[int(result_tmp)-1],choice_tmp[int(result_tmp)-1]]
					else:
						result_tmp = answer_tmp[int(result_tmp)-1]
					passed = True
			else:
				if result_tmp != '':
					passed = True
					if 'tester' in question:
						if question['tester'][1]:
							vars_to_send = [result_tmp]
							for var in question['tester'][1]:
								vars_to_send.append(var)
							passed = question['tester'][0](*vars_to_send)
						else:
							passed = question['tester'][0](result_tmp)
				else:
					if 'default' in question:
						result_tmp = question['default']
						passed = True

			if passed:
				if result_tmp not in [False,None]:
					if 'format' in question:
						if question['format'] ==int:
							result_tmp = int(result_tmp)
						if question['format'] ==float:
							result_tmp = float(result_tmp)
						if question['format'] == 'osc_args':
							result_tmp = convert_to_appropriate_type(result_tmp)
				if result_tmp != None:
					dest[model] = result_tmp
			else:
				os.system('cls')
				print(quest_out)
				result_tmp = "Skipping that question" if result_tmp == "" else result_tmp
				pass
				speak(f"{result_tmp} is not a valid choice. Let me repeat the question. {quest_out} Try again?")

	#os.system('cls')
