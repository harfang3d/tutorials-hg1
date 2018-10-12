-- How to retrieve information on the system input devices

hg = require("harfang")

device_typename = {'Unknown', 'Keyboard', 'Mouse', 'Pad', 'Touch', 'HMD', 'Controller'}

-- retrieve the list of all available devices on the system
devices = hg.GetInputSystem():GetDevices()

-- print it to screen
print("The following devices are available on this system:")

for i=0,(devices:size()-1) do
	local device_name = devices:at(i)
	local device_type = hg.GetInputSystem():GetDevice(device_name):GetType()
	print(string.format('- %s (name: "%s")', device_typename[device_type+1], device_name))
end