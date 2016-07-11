# How to read values from the mouse

import gs

renderer = gs.EglRenderer()
renderer.Open(480, 240)

# continue while the window is open
print("Click the left mouse button to print the current mouse cursor position")
print("Close the renderer window or press Ctrl+C in this window to end")

while renderer.GetDefaultOutputWindow():
	# get the mouse device
	mouse_device = gs.GetInputSystem().GetDevice("mouse")

	# check if left button is down
	if mouse_device.IsButtonDown(gs.InputDevice.Button0):
		# get the mouse position in the window ([0, 1])
		print("Mouse X: %f, Mouse Y: %f" % (mouse_device.GetValue(gs.InputDevice.InputAxisX), mouse_device.GetValue(gs.InputDevice.InputAxisY)))

	# update window
	renderer.DrawFrame()
	renderer.ShowFrame()
	renderer.UpdateOutputWindow()
