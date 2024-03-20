from pyfirmata import Arduino, util
import time

# Define the serial port for your Arduino
port = 'COM3'

# Connect to the Arduino
board = Arduino(port)

# Define a function to blink an LED
def blink_led(pin, delay_time):
	while True:
		board.digital[pin].write(1)  # Turn the LED on
		time.sleep(delay_time)
		board.digital[pin].write(0)  # Turn the LED off
		time.sleep(delay_time)

# Define the pin number for the LED
led_pin = 13  # Assuming you have an LED connected to pin 13

# Call the blink_led function with the LED pin and delay time (in seconds)
blink_led(led_pin, 3)
