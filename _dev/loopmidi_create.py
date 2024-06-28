import rtmidi

# Create a virtual MIDI port
def create_virtual_port(port_name):
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()

    # Check if the port already exists
    for port in available_ports:
        if port_name in port:
            print("Virtual MIDI port already exists:", port)
            return port

    # Create a new virtual port
    midi_out.open_virtual_port(port_name)
    print("Virtual MIDI port created:", port_name)
    return port_name

# Specify the name of your virtual MIDI port
virtual_port_name = "MyVirtualMIDIPort"

# Create the virtual MIDI port
virtual_port = create_virtual_port(virtual_port_name)