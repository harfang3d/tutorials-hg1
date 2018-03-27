# How to read values from a game controller

import harfang as hg

hg.LoadPlugins()

plus = hg.GetPlus()
plus.RenderInit(400, 300)

device = hg.GetInputSystem().GetDevice("xinput.port0")

# continue while the window is open
while not plus.IsAppEnded():
	# check if left button is down
	for i in range(hg.Button0, hg.ButtonLast):
		if device.WasButtonPressed(i):
			print("%d was pressed" % i)

	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()