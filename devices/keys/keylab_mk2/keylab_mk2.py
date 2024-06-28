def pre_midi(self,msg):

	if msg.channel == 9:
		msg.channel = 0
	
	if msg.channel == 0:

		if msg.type == 'control_change':

			if msg.control in[11,12,13]:

				inverted_polarity = [True,False,False]
				if msg.value in[0,127]:
					if inverted_polarity[msg.control-11]:
						msg.value = 0 if msg.value == 127 else 127
					self.control_assoc.matrix_send([[msg.control+490,[]],True if msg.value == 127 else False,msg.value])
			
				passed = False

		

data = {
	'name' : "Arturia KeyLab Mk2",
	'ports' : ['KeyLab mkII','KeyLab mkII','startswith'],
	'settings':{
		'control_assoc':'keylab_mk2',
	},
	'pre_midi':[pre_midi,True],
}