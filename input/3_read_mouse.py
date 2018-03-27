# How to read values from the mouse

import harfang as hg

hg.LoadPlugins()

plus = hg.GetPlus()
plus.RenderInit(400, 300)

# continue while the window is open
print("Click the left mouse button to print the current mouse cursor position")
print("Close the renderer window or press Ctrl+C in this window to end")

while not plus.IsAppEnded():
	# get the mouse device
	mouse_device = hg.GetInputSystem().GetDevice("mouse")

	# check if left button is down
	if mouse_device.IsButtonDown(hg.Button0):
		# get the mouse position in the window ([0, 1])
		print("Mouse X: %f, Mouse Y: %f" % (mouse_device.GetValue(hg.InputAxisX), mouse_device.GetValue(hg.InputAxisY)))

	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()