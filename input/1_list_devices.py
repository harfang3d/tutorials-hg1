# How to retrieve information on the system input devices

import harfang as hg

device_typename = ['Unknown', 'Keyboard', 'Mouse', 'Pad', 'Touch', 'HMD', 'Controller']

# retrieve the list of all available devices on the system
devices = hg.GetInputSystem().GetDevices()

# print it to screen
print("The following devices are available on this system:")

for device_name in devices:
	device_type = hg.GetInputSystem().GetDevice(device_name).GetType()
	print('- %s (name: "%s")' % (device_typename[device_type], device_name))
