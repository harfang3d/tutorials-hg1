import gs

plus = gs.GetPlus()
plus.RenderInit(400, 300)

while not plus.KeyPress(gs.InputDevice.KeyEscape):
	plus.Flip()
