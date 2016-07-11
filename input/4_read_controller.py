# How to read values from a game controller

import gs

renderer = gs.EglRenderer()
renderer.Open(480, 240)

device = gs.GetInputSystem().GetDevice("xinput0")

# continue while the window is open
while renderer.GetDefaultOutputWindow():
	# check if left button is down
	for i in range(14):
		if device.WasButtonPressed(gs.InputDevice.Button0 + i):
			print("%d was pressed" % i)

	# update window
	renderer.DrawFrame()
	renderer.ShowFrame()
	renderer.UpdateOutputWindow()
