# How to retrieve information on the system input devices

import gs

# retrieve the list of all available devices on the system
devices = gs.GetInputSystem().GetDevices()

# print it to screen
print("The following devices are available on this system:")

for device in devices:
	print('- %s (name: "%s")' % (device.GetId(), device.GetName()))
