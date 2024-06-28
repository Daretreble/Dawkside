import math

def value_from_normalized(value, min_val, max_val):
	return round(value * (max_val - min_val) + min_val, 4)

def normalized_from_min_max(value,min_val,max_val):
	try:
		return round((value - min_val) / (max_val - min_val),4)
	except:
		pass

def convert_to_appropriate_type(input_str):
	
	if input_str.isdigit():  # Check if the input is a positive integer
		return int(input_str)
	
	try:
		float_val = float(input_str)  # Try converting to float
		return float_val
	except ValueError:
		pass
	
	if input_str.lower() == 'true':
		return True
	elif input_str.lower() == 'false':
		return False
	
	if input_str.startswith('(') and input_str.endswith(')'):
		try:
			tuple_val = tuple(map(eval, input_str[1:-1].split(',')))  # Attempt to create a tuple
			return tuple_val
		except Exception:
			pass
	
	if ',' in input_str:
		try:
			list_val = list(map(eval, input_str.split(',')))  # Attempt to create a list
			return list_val
		except Exception:
			pass
	
	return input_str  # If none of the conversions match, return the original string

def merge_dicts(*dicts):
	result_dict = {}
	
	for d in dicts:
		for key, value in d.items():
			if key in result_dict and isinstance(value, dict) and isinstance(result_dict[key], dict):
				# If the key exists in result_dict and both values are dictionaries, merge them
				result_dict[key] = merge_dicts(result_dict[key], value)
			else:
				# Otherwise, update the key in result_dict
				result_dict[key] = value

	return result_dict

def keys_to_int(json_data):
    if isinstance(json_data, dict):
        new_dict = {}
        for key, value in json_data.items():
            try:
                new_key = int(key)
            except ValueError:
                new_key = key
            new_value = keys_to_int(value)
            new_dict[new_key] = new_value
        return new_dict
    elif isinstance(json_data, list):
        return [keys_to_int(item) for item in json_data]
    else:
        return json_data

def dict_test(d, keys):
	if not keys:
		return True
	if isinstance(d, dict):
		first_key = keys[0]
		if first_key in d:
			return dict_test(d[first_key], keys[1:])
	return False

def update_multi_level_dict(original_dict, new_dict):
	for key, new_value in new_dict.items():
		if key in original_dict and isinstance(original_dict[key], dict) and isinstance(new_value, dict):
			update_multi_level_dict(original_dict[key], new_value)
		else:
			original_dict[key] = new_value

def model_rotary_menus(info):
	
	model = info[0][1]['model']
	value = info[2]
	
	if model[:1] == 'r':

		if model == 'r1':
			if value in range(107,128):
				repeats = value-126
				dir = False
			if value in range(20):
				repeats = value
				dir = True
	
		if model == 'r2':
			if value in range(65,85):
				repeats = value-64
				dir = False
			if value in range(20):
				repeats = value
				dir = True
		
		return dir,repeats

def smooth_increment(speed, multiplier):
	
	normalized_speed = (speed - 1) / 29
	incremented_speed = normalized_speed * multiplier
	smoothed_increment = math.pow(incremented_speed, 2)
	return smoothed_increment

def scale_velocity(min_velocity, max_velocity, actual_velocity):

	if actual_velocity < min_velocity:
		return min_velocity
	elif actual_velocity > max_velocity:
		return max_velocity

	scaled_velocity = ((actual_velocity - min_velocity) / (max_velocity - min_velocity)) * (max_velocity - min_velocity) + min_velocity
	return int(scaled_velocity)

def model_convert(model,value,last_value):
	
	output_value = False
	multiplier = 20
	ratio = 0.01
	tolerance = 30
	
	if model == 'cc':
		output_value = pitch_convert('c2v',value)
		
	if model == 'p1':
		output_value = pitch_convert('p12v',value)
		
	if model[:1] == 'r':
		
		speed = [0,False]
		
		if model == 'r1':
			if value in range(tolerance):
				speed = [value,'up']
			if value in range(128-tolerance,128):
				speed = [127-value,'down']
				
		if model == 'r2':
			if value in range(tolerance):
				speed = [value,'up']
			if value in range(65,65+tolerance):
				speed = [value-65,'down']
		
		if speed[0] <= tolerance:
			inc = smooth_increment(speed[0],multiplier) * ratio
			output_value = last_value + inc if speed[1] == 'up' else last_value - inc
	
	if output_value:
		output_value = max(0.0, min(output_value, 1.0))
		return round(output_value,4)
	else:
		return False

def find_position(number):
    
	bank = number // 8
	position = number % 8

	return [position, bank]

def bank_position(range,bank,num):

	start = range[0]
	end = range[1]
	num_banks = (end - start + 1) // bank
    
	if num < start or num > end:
		return False
    
	position = (num - start) // bank
	return position

def pitch_convert(*args):
	
	"""
	Converts different data types.
	c = cc (0,127)
	p = pitchwheel (-8191-8192)
	v = values from 0 to 1
	"""
	
	type = args[0]
	value = args[1]
	
	# Normalized value to pitchwheel
	if type == 'v2p1':
		return int((value * 16383) - 8192)
		
	# Normalized value to cc
	if type == 'v2c':
		return int(value * 127)
	
	# pitchwheel to normalized value
	if type == 'p12v':
		return float((value + 8192) / 16383)
	
	# pitchwheel to midi cc
	if type == 'p2c':
		return int(((value + 8192) / 16383) * 127)
	
	# midi cc to pitchwheel
	if type == 'c2p':
		return int((value / 127) * 16383) - 8192
	
	# midi cc to normalized value
	if type == 'c2v':
		return float(value / 127.0)

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
octaves = list(range(11))
notesInOctave = len(notes)

def number_to_note(number: int) -> tuple:

	""" Converts note number to note name """
	
	octave = number // notesInOctave
	note = notes[number % notesInOctave]
	return note, octave

def note_to_number(note: str, octave: int) -> int:

	""" Converts note name to number. """

	note = notes.index(note)
	note += (notesInOctave * octave)

	return note
	
def invert_grid_position(position):

	""" Inverts 0-64 to 64-0 grids and also returns column and row. """

	row = 7 - (position // 8)
	col = position % 8
	inverted_position = (row * 8) + col
	return [inverted_position,col,row]
