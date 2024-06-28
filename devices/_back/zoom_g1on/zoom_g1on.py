def pre_midi(self,msg):

	print(msg)

data = {
	'name' : "Zoom G1On",
	'ports' : ['ZOOM 1 Series','ZOOM 1 Series','startswith'],
	'settings':{
		'control_assoc':'keylab_mk2',
	},
	#'pre_midi':[pre_midi,True],
}