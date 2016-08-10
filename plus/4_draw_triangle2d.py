import gs

plus = gs.GetPlus()
plus.RenderInit(400, 300)

while not plus.KeyPress(gs.InputDevice.KeyEscape):
	plus.Clear()
	plus.Triangle2D(40, 40, 200, 260, 360, 40, gs.Color.Red, gs.Color.Blue, gs.Color.Green)
	plus.Flip()
