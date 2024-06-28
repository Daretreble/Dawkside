import mido
import threading

# Create a flag to control the loop
keep_running = True

# Function to handle MIDI messages
def midi_listener(port):
    global keep_running
    for msg in port:
        print(msg)  # Process the received MIDI message here
        # Check for conditions to exit the loop
        if not keep_running:
            break

# Open the MIDI port
with mido.open_input('Your_MIDI_Port_Name') as port:
    # Create a thread for MIDI message handling
    midi_thread = threading.Thread(target=midi_listener, args=(port,))
    midi_thread.start()

    # Perform other operations while listening to MIDI
    # For instance, you could wait for a user input to stop the thread
    input("Press Enter to stop: ")

    # Set the flag to stop the loop
    keep_running = False

# Wait for the thread to finish
midi_thread.join()