import time
from .classes import *
from classes.track.track import Track
from classes.tracks.tracks import Tracks
from classes.plugins.plugins import Plugins
from classes.transport.transport import Transport
from .classes import *
from .functions import *
from functions.speak import speak

class Live:
	""" Control Live calls. """
	
	def __init__(self,main):
		self.name = "AbletonLive"
		self.short_name = 'live'
		self.developer = ["Ableton"]
		self.switch_on = True
		self.switch_delay = 0.2
		self.fre = {
			'track':False,
			'tracks':False,
			'plugins':False,
			'ccs':False,
		}		
		self.tracks = Tracks(self)
		self.track = Track(self)
		self.triggers = {
			'transport':{
				93:['stop',['/live/song/get/is_playing',False],['/live/song/stop_playing',()],False,False],
				94:['play',['/live/song/get/is_playing',True],['/live/song/start_playing',()],False,['Playing','Stopped']],
				98:['metronome',['/live/song/get/metronome',True],[['/live/song/set/metronome',True],['/live/song/set/metronome',False]],False,['Metronome on','Metronome off'],['Metronome off','Metronome on']],
				1100:['session_record',['/live/song/get/session_record',True],['/live/song/trigger_session_record',()],False,['Session record on','Session record off'],['Session record','Stopped recording']],
			},
			'track_toggle':{
				'solo':[70,True,False],
				'mute':[71,False,False],
				'arm':[72,True,False],
			},
			'track_toggle_ids':{},

		}
		self.triggers['track_toggle_ids'] = {value[0]: key for key, value in self.triggers['track_toggle'].items()}
		self.main = main
		self.plugins = Plugins(self)
		self.scenes = Scenes(self)
		self.clips = Clips(self)
		self.session = Session(self)
		self.transport= Transport(self)
		self.online = {'control':[],'keys':[]}
		self.modes = {
			100:{'name':'Dashboard','desc':"Live's Dashboard mode encompasses all the tools necessary for software navigation, accessing various functions, and configuring settings."},
			101:{'name':"Track",'assoc':11,'desc':"Live's Track mode allows you to manage the volume, pan, sends, and receives of the selected track."},
			102:{'name':"Plugins",'assoc':12,'desc':"Live's Plugins mode is the all-in-one tool for controlling selected track plugins, their parameters, and accessing various useful plugin-related functionalities."},
			103:{'name':"Mixer",'assoc':13,'desc':"Live's Mixer mode."},
			}
		self.datatmp = {
			'first_load':True,
			'first_pass_startup':True,
			'osc_tracking':{
				'watched_tracks':[],
				'scene_change':[True,time.time()],
				'track_change':[True,time.time()],
				'page_change':[False,time.time()],
				'page_load':[False,time.time()],
				'devices_check':[False,time.time()],
			},
			'listens':{
				'parameters':[],
			},
		}
		self.song_listeners = {
			'tempo':[False],
			'is_playing':[False],
			'metronome':[False],
			'session_record':[False],
		}
		self.exclusive = {
			'track_offset':0,
			'scene_offset':0,
			'tempo_reporting':True,
		}
	def track_select(self,*args,**kwargs):

		action = kwargs['action']
		
		if action == 'nav':
			
			dir = args[0]
			new_track = self.track.index[0] + dir
			if new_track in range(0,self.tracks.num[0]):
				self.client.send_message('/live/view/set/selected_track',new_track)
	
	def fake_valstr(self,pos,value):
		if pos in range(6) or pos == 7:
			return str(round(value*100)) + "percent"
		elif pos == 6:
			pan_tmp = round(value*100)
			return str(pan_tmp)

# Functions
Live.command_launch = command_launch
Live.devices_manage = devices_manage
Live.get_data = get_data
Live.midi_loop = midi_loop
Live.osc = osc
Live.process_loop = process_loop
Live.refresh = refresh
Live.startup = startup