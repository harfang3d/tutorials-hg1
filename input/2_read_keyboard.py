# How to read from the keyboard

import harfang as hg

hg.LoadPlugins()

plus = hg.GetPlus()
plus.RenderInit(400, 300)

# retrieve the keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

print("Press 'X' to exit")

while not plus.IsAppEnded():
	# catch the exit key
	if keyboard.WasPressed(hg.KeyX):
		break

	# log key presses
	for key in range(hg.KeyLast):
		if keyboard.WasPressed(key):
			print("Keyboard key pressed: %d" % key)

	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()