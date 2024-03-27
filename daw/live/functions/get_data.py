import time

def get_data(self):
	""" Sets Live's data. """

	tracks = self.tracks
	scenes = self.scenes
	
	self.tracks.offset = 0
	self.scenes.offset = 0
	# Listeners
	for _ in self.song_listeners:
		self.client.send_message('/live/song/start_listen/'+_,())
	self.client.send_message('/live/view/start_listen/selected_scene',())
	self.client.send_message('/live/view/start_listen/selected_track',())
	
	"""
	for _ in range(8):
		self.client.send_message('/live/track/start_listen/playing_slot_index',(_))
		self.client.send_message('/live/track/start_listen/fired_slot_index',(_))
	"""