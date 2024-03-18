import bluetooth

def get_connected_devices():
    connected_devices = []
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in nearby_devices:
        if bluetooth.lookup_name(addr) is not None:
            connected_devices.append((addr, name))
    return connected_devices

connected_devices = get_connected_devices()
for device in connected_devices:
    print("Address:", device[0], "Name:", device[1])
