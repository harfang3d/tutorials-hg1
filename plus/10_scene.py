import gs

plus = gs.GetPlus()
plus.RenderInit(640, 400)

scn = plus.NewScene()

cam = plus.AddCamera(scn, gs.Matrix4.TranslationMatrix((0, 1, -10)))
plus.AddLight(scn, gs.Matrix4.TranslationMatrix((6, 4, -6)))
plus.AddCube(scn, gs.Matrix4.TranslationMatrix((0, 0.5, 0)))
plus.AddPlane(scn)

fps = gs.FPSController(0, 2, -10)

while not plus.KeyPress(gs.InputDevice.KeyEscape):
	dt = plus.UpdateClock()

	fps.UpdateAndApplyToNode(cam, dt)

	plus.UpdateScene(scn, dt)
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around")
	plus.Flip()
