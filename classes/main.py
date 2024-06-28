import sys
import os
import time
from functions.speak import speak
import pygame
import threading

class Main:
	""" Global """
	def __init__(self):
		self.queries = sys.argv
		self.safety_guards = {
			'question_access': [False,"Please leave the actual questionnaire by entering 'exit' and press Enter in the console."]
		}
		self.running_threads_on = True
		self.midi_ports = []
		self.locked = [True,'']
		self.loading = True
		self.switchtime = time.time()
		self.daws = {}
		self.daws_index = []
		self.devices = {
			'control':{},
			'keys':{},
			'ports':{},
		}
		self.modifiers_data = {
			'status':[False,[]]
			,
			'list':{
				900:[False,'Shift'],
				901:[False,'Mod One'],
				902:[False,'Mod Two'],
				903:[False,'Mod Three'],
				904:[False,'Select'],
				905:[False,'Alt'],
				906:[False,'Control'],
				907:[False,'Switch'],
				908:[False,'Add'],
				909:[False,'Delete'],
				910:[False,'Add'],
				911:[False,'Help'],
				921:[False,False],
				922:[False,False],
				923:[False,False],
				924:[False,False],
			}
		}
		self.outmodes = {
			10:{'name':"Midi (to come)",'type':'midicc','desc':"The MIDI output mode allows you to utilize your faders and encoders to send MIDI CC messages to the DAW."},
			11:{'name':"Track",'type':'track','desc':"The Track output mode assigns the faders and encoders to control various parameters such as volume, pan, sends, and more for the selected track."},
			12:{'name':"Plugins",'type':'plugins','desc':"The Plugins output mode directs the faders and encoders to control all plugin parameters."},
			13:{'name':"Mixer (to come)",'type':'tracks','desc':"The mixer output mode enables you to utilize the faders and encoders as a multi-track control surface."},
			14:{'name':"Midi routing (to come)",'type':'routing','desc':"The MIDI Routing mode is a powerful tool that empowers you to route various MIDI signals to other devices and DAWs."},
		}
		pygame.mixer.init()  # Initialize Pygame mixer

	def safety_check(self, guard):
		if self.safety_guards[guard][0]:
			speak(self.safety_guards[guard][1])
			return False
		else:
			return True
			
	def game_over(self):
		self.running_threads_on = False
		for ml in self.midi_ports:
			ml.close()
			
		# Shutdown osc server
		for key,value in self.daws.items():
			value.server.shutdown()
		speak("Exiting Dawkside. See.")
		time.sleep(1)
	
	def modif(self, action, *args):
	
		data = self.modifiers_data
		list = data['list']
		status = data['status']
		
		if action == 'status':
			return [False if len(status[1]) == 0 else True,status[1]]
		
		if action == 'test':
			return all(number in status[1] for number in args[0])
		
		if action == 'trig':
			id = args[0]
			state = args[1]
			if state:
				if id not in status[1]:
					status[1].append(id)
					if list[id][1]:
						speak(list[id][1])
			else:
				if id in status[1]:
					status[1].remove(id)
		
	def play_sound(self, sound):
		def play(sound):
			sound_path = os.path.join('media','sounds',sound+".mp3")
			pygame.mixer.Sound(sound_path).play()
		
		threading.Thread(target=play, args=(sound,)).start()