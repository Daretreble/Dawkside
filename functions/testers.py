import json

def osc_args_check(to_test):
	return True

def json_check(to_test):
	try:
		converted_dict = json.loads(to_test)
		return True
	except json.JSONDecodeError as e:
		return False

def command_check(id):
	if id.isdigit():
		number = int(id)
		if 0 <= number < 3000:
			return True
	return False

def param_check(id,params):
	return True if int(id) in params else False

def normalized_check(normalized):
	try:
		value = float(normalized)
		return 0.0 <= value <= 1.0
	except ValueError:
		return False

def seven_bit_check(value):
	try:
		value = int(value)
		return 0 <= value <= 127
	except (ValueError, TypeError):
		return False

def four_bit_check(value):
	try:
		value = int(value)
		return 0 <= value <= 15
	except (ValueError, TypeError):
		return False

def sysex_check(data):
	return True