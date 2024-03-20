import time
from pyfirmata import Arduino, util

# Define the pins for the potentiometers
pot_pins = [0]

# Set up the board
board = Arduino('COM3')  # Change this to match your Arduino's serial port
iterator = util.Iterator(board)
iterator.start()
iterator.enable_reporting()

# Define the range for the potentiometers
min_value = 0
max_value = 1023  # Potentiometers typically output a range from 0 to 1023
mapped_min = 0.0
mapped_max = 1.0

# Function to map values from one range to another
def map_value(value, from_low, from_high, to_low, to_high):
	return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# Initialize an array to store the current values of the potentiometers
pot_values = [0.0] * len(pot_pins)

try:
	while True:
		for i, pin in enumerate(pot_pins):
			pot_value = board.analog[pin].read()  # Read the analog value from the potentiometer
			if pot_value is not None:
				mapped_value = map_value(pot_value, min_value, max_value, mapped_min, mapped_max)
				pot_values[i] = round(mapped_value, 2)  # Round to two decimal places
				print(f'Potentiometer {i+1}: {pot_values[i]}')
		time.sleep(0.05)  # Wait for 0.05 seconds before reading values again

except KeyboardInterrupt:
	board.exit()