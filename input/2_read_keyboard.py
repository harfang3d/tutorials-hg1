# How to read from the keyboard

import gs

# retrieve the keyboard device
keyboard = gs.GetInputSystem().GetDevice("keyboard")

print("Press 'X' to exit")

while True:
	# catch the exit key
	if keyboard.WasPressed(gs.InputDevice.KeyX):
		break

	# log key presses
	for key in range(gs.InputDevice.KeyLast):
		if keyboard.WasPressed(key):
			print("Keyboard key pressed: %d" % key)
