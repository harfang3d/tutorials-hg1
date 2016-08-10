import gs

plus = gs.GetPlus()
plus.RenderInit(400, 300)

angle = 0
cube = plus.CreateGeometry(plus.CreateCube())

while not plus.KeyPress(gs.InputDevice.KeyEscape):
	plus.Clear()
	plus.Geometry2D(200, 150, cube, angle, angle * 2, 0, 100)
	plus.Flip()

	angle += 0.01
