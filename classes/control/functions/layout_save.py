# Saves layots

import os
import json

def layout_save(self):
	
	with open(os.path.join('devices','control',self.short_name,'layouts','default.json'), 'w') as file:
		json.dump(self.layouts, file,indent=0)
	