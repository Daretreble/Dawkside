def pre_midi(self,msg):

	pass

data = {
	'name' : "Korg D1",
	'ports' : ['4- UM-ONE','4- UM-ONE'],
	'settings':{
		'control_assoc':'apc_mini',
	},
	'pre_midi':[pre_midi,True],
}