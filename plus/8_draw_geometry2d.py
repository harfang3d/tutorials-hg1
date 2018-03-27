import harfang as hg

hg.LoadPlugins()

plus = hg.GetPlus()
plus.RenderInit(400, 300)

angle = 0
cube = plus.CreateGeometry(plus.CreateCube())

while not plus.IsAppEnded():
	plus.Clear()
	plus.Geometry2D(200, 150, cube, angle, angle * 2, 0, 100)
	plus.Flip()
	plus.EndFrame()

	angle += 0.01

plus.RenderUninit()