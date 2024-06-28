import copy
from functions.speak import speak

def zone_manage(self,*args,**kwargs):
	""" Keys zones management. """
	main = self.main
	modif = main.modif
	daw = self.control_assoc.daw
	plugins = daw.plugins

	if 'action' in kwargs:
		action = kwargs['action']
	#else:
		#action = args[2]
	
	assoc = self.control_assoc
	
	if action != 'refresh':
		zone = args[0]
		refresh = False
	
	if action == 'zoneprompt':
		os.system('cls')
		
		quest = "Low note: "
		self.zones_config[zone][1] = int(input(quest) or 0)
		speak(quest)
		
		quest = "High note: "
		self.zones_config[zone][2] = int(input(quest) or 127)
		speak(quest)
		
		quest = "Transpose: "
		self.zones_config[zone][3] = int(input(quest) or 0)
		speak(quest)
		
		quest = "Sustain: (Enter 'yes' or press Enter for 'no'"
		sustmp = input(quest)
		speak(quest)
		
		self.zones_config[zone][5] = True if sustmp == 'yes' else False
		self.zones_config[zone][0] = True
		
		os.system('cls')
		speak(f"Zone {zone+1} added.")
	
	if action == 'pluginzoneclear':
	
		if modif('test',[911]):
			
			speak("Reset saved zones for that plugins.")
			
		else:
		
			if plugins.act:
			
				if plugins.user.is_saved('plugin'):
				
					plugins.user_params[plugins.name]['zones'] = {}
					plugins.user.param_save()
					
					#keyst(self,False,0,'zonepreset',speak=False)
					
					speak(f"Zones resetted for {self.name}")
				
			else:
			
				speak("Please insert a plugin.")
	
	if action == 'pluginzonesave':
	
		if modif('test',[911]):
		
			speak(f"Save zones for that plugin.")
		
		else:
		
			if plugins.act:
			
				if not plugins.user.is_saved('plugin'):
				
					plugins.user.page_create()
			
				tmp = plugins.user_params[plugins.name]['zones']
				
				zonetmp = copy.deepcopy(self.zones_config)
				
				if plugins.subname not in tmp:
					tmp[plugins.subname] = {self.short_name:zonetmp}
				else:
					if self.name not in tmp[plugins.subname]:
						tmp[plugins.subname][self.short_name] = zonetmp
					else:
						tmp[plugins.subname].update({self.short_name:zonetmp})
				
				plugins.user.param_save()
				
				speak("Transposition zones saved on "+self.name+" using "+plugins.fullname)
				
			else:
			
				speak("Please insert a Plugin to save a default zone")
	
	if action == 'trackzonesave':
	
		if modif('test',[911]):
			speak(f"Save zones for that track.")
		else:
			
			zonetmp = copy.deepcopy(self.zones_config)
			tmp = daw.track.history[daw.track.reapy_track.id]['tr']
	
			if self.short_name not in tmp:
				tmp[self.short_name] = zonetmp
			else:
				tmp.update({self.short_name:zonetmp})
			
			speak('Zone saved')
	
	if action == 'zonesustain':
	
		if modif('test',[911]):
		
			speak(f"{'Enable' if args[1] > 0 else 'Disable'} sustain for zone {zone+1}")
		
		else:
		
			if zone < len(self.zones_config):
		
				self.zones_config[zone][5] = args[1]
				speak(f"Sustain pedal {'active' if self.zones_config[zone][5] else 'inactive'} for zone {zone+1}")
	
	if action == 'zonechanneldirect':
	
		if modif('test',[911]):
			speak(f"Assign zone {zone+1} to channel {args[1]}")
		else:
			self.zones_config[zone][4] = args[1]
			speak(f"Channel changed")
	
	if action == 'split':
	
		ref = args[0]
		
		if modif('test',[911]):
		
			speak(f"Split keyboard and add a zone before note {ref}")
		
		else:
		
			for _ in self.zones_config:
				if ref in range(_[1],_[2]):
					min = _[1]
					max = _[2]
					self.zones_config.append(
						[True,min,ref-1,0,len(self.zones_config),True]
					)
					_[1] = ref
					
					
			speak("Keyboard splitted")
	
	if action == 'zonepreset':
		
		preset = args[0]
		presets = self.zone_presets
		
		if modif('test',[911]):
		
			if preset < len(presets):
				speak(f"Load preset named {presets[preset][1]}")
			else:
				speak("Add a preset to the code to make it available here.")
		
		else:
		
			if preset < len(presets):
			
				self.zones_config = presets[preset][0]
			
				if 'speak' not in kwargs:
					speak(presets[preset][1])
			else:
				speak("No preset.")
	
	if action == 'zonetranspose':
	
		if zone+1 <= len(self.zones_config) and self.zones_config[zone][0]:
			if modif('test',[911]):
				speak(f"Transpose zone {zone+1} {'up' if args[1] > 0 else 'down'} one octave")
			else:
				if args[1] < 0 and self.zones_config[zone][3] > -3:
					self.zones_config[zone][3]+=args[1]
				if args[1] > 0 and self.zones_config[zone][3] < 4:
					self.zones_config[zone][3]+=args[1]
				speak(f"{self.zones_config[zone][3]} on zone {zone+1}.")
				
		else:
			speak(f"Zone {zone+1} not defined.")
		
	if action == 'zonetransposereset':
	
		if modif('test',[911]):
			speak(f"Reset zone {zone+1}.")
		else:		
			if zone+1 <= len(self.zones_config):
				self.zones_config[zone][3] = 0
				speak(f"Zone {zone+1} resetted.")
			else:
				speak(f"Zone {zone+1} not defined.")
		
	if action == 'zonechannel':
	
		if modif('test',[911]):
		
			speak(f"{'Increase' if args[1] > 0 else 'Decrease'} channel for zone {zone+1}.")
		
		else:
		
			if zone < len(self.zones_config):
			
				ch = self.zones_config[zone][4] + args[1]
			
				if ch in range(0,16):
					self.zones_config[zone][4]+=args[1]
				
				speak(f"Channel {self.zones_config[zone][4]+1} on zone {zone+1}")
	
	if action == 'zonedel':
	
		if self.zones_config[zone][0]:
			self.zones_config[zone] = [False,False,False,0,self.zones_config[zone][4],False]
			speak(f"Zone {zone+1} deleted.")
		else:
			speak(f"Zone {zone+1} not set.")
	
	if action == 'zoneset':
	
		if len(assoc.NTon) > 0:
			note = assoc.NTon[-1]
			lowhi = args[1]
			zonetmp = self.zones_config[zone]
			
			self.zones_config[zone][0] = True
			self.zones_config[zone][lowhi] = note
			speak(f"Position {lowhi} of zone {zone+1} is {Main.number_to_note(note)}")
		else:
			speak(f"Press a note on {assoc.name}")
	
	self.panic()
	
	"""			
	for m in Main.onlinedev:
	
		if m.keys and m.keys == assoc:
		
			if m.mode in[6,67]:
				for _ in range(48,56):
					m.mtxin(m.mode,_,'znprst',action='unit')
			
			for _ in range(4):
			
				if m.mode == 6 or (m.mode == 67 and _ == 0):
				
					zc = m.keys.zoneconf[_]
					
					if m.mode == 6:
						m.mtxin(m.mode,32+_,'znsustain' if (zc[5] and zc[0]) else 'znon' if zc[0] else 'znoff',action='unit')
						m.mtxin(m.mode,24+_,'znznon' if zc[2] != False or str(zc[1]) == '0' else 'znznoff',action='unit')
						m.mtxin(m.mode,16+_,'znznon' if zc[1] != False or str(zc[1]) == '0' else 'znznoff',action='unit')
					m.mtxin(m.mode,8+_,'zntron' if zc[3] > 0 else 'zntroff',action='unit')
					m.mtxin(m.mode,0+_,'zntron' if zc[3] < 0 else 'zntroff',action='unit')		

	"""