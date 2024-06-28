import accessible_output2.outputs.auto
accessOut = accessible_output2.outputs.auto.Auto()

OLDSPEAK = ''

def speak(toSpeak,printout=False,repeat=True,interrupt=True):
	""" Manages all speech. """
	global OLDSPEAK
	if toSpeak != OLDSPEAK or repeat:
		accessOut.speak(str(toSpeak), interrupt=interrupt)
		OLDSPEAK = toSpeak
		if printout:
			print(toSpeak)