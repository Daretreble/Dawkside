import time
from .classes import *
from classes.track.track import Track
from classes.tracks.tracks import Tracks
from classes.plugins.plugins import Plugins
from classes.transport.transport import Transport
from .functions import *
from functions.speak import speak

class Reaper:
	""" Control Reaper calls. """
	
	def __init__(self,main):
		self.reapy_mode = True
		self.name = "Reaper"
		self.short_name = 'reaper'
		self.developer = ["Cockos","www.reaper.fm"]
		self.switch_on = True
		self.switch_delay = 0.4
		self.tempo_reporting = False
		self.transpose_save = False
		self.triggers = {
			'transport':{
				93:['stop',['/stop',1.0],['/action',1016],False,False,['Playing','Stopped']],
				94:['play',['/play',1.0],['/action',40044],False,False,['Stopped','Playing']],
				95:['record',['/record',1.0],['/action',1013],False,False,['Not recording','Recording']],
				98:['metronome',['/click',1.0],['/action',40364],False,False,['Metronome off','Metronome on']],
				102:['repeat',['/repeat',1.0],['/action',1068],False,False,['Repeat off','Repeat on']],
				103:['readwrite',['/track/autolatch',1.0],[['/action',40266],['/action',40086]],False,['Latch','Read'],['Read on all tracks','Latch on all tracks']],
			}
		}
		self.fre = {
			'track':False,
			'tracks':False,
			'plugins':False,
			'ccs':False,
		}
		self.main = main
		self.track = Track(self)
		self.tracks = Tracks(self)
		self.plugins = Plugins(self)
		if not self.reapy_mode:
			self.plugins.sendrecv_tmp = {}
			for cat in ['send','recv']:
				self.plugins.sendrecv_tmp[cat] = {}
				for _ in range(6):
					self.plugins.sendrecv_tmp[cat][_+1] = {'pitch':[],'name':'','valstr':''}
					

		self.transport= Transport(self)
		self.online = {'control':[],'keys':[]}
		self.modes = {
			100:{'name':'Dashboard','desc':"The Reaper's Dashboard mode encompasses all the tools necessary for software navigation, accessing various functions, and configuring settings."},
			101:{'name':"Track",'assoc':11,'desc':"The Reaper's Track mode allows you to manage the volume, pan, sends, and receives of the selected track."},
			102:{'name':"Plugins",'assoc':12,'desc':"Reaper's Plugins mode is the all-in-one tool for controlling selected track plugins, their parameters, and accessing various useful plugin-related functionalities."},
			103:{'name':"Mixer",'assoc':13,'desc':"Reaper's Mixer mode."},
			}
		self.exclusives = {
			'track_offset':0,
			'scene_offset':0,
			'send_recv_sel':'send',
		}

	def quit(self):
		
		self.pVar = ['quit']
		self.routing.inport.close()
		self.routing.outport.close()
		self.routing = False
		self.server.shutdown()
		time.sleep(3)
		del(self.main.daws['reaper'])
		speak("Reaper has left the building",printout=True)

# Functions
Reaper.command_launch = command_launch
Reaper.get_data = get_data
Reaper.midi_loop = midi_loop
Reaper.osc = osc
Reaper.refresh = refresh
Reaper.startup = startup
Reaper.status_loop = status_loop