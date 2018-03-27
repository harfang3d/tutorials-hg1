import harfang as hg

hg.LoadPlugins()

plus = hg.GetPlus()
plus.RenderInit(640, 400)

scn = plus.NewScene()

cam = plus.AddCamera(scn,hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1, -10)))
plus.AddLight(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(6, 4, -6)))
plus.AddCube(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 0.5, 0)))
plus.AddPlane(scn)

fps = hg.FPSController(0, 2, -10)

while not plus.IsAppEnded():
	dt = plus.UpdateClock()

	fps.UpdateAndApplyToNode(cam, dt)

	plus.UpdateScene(scn, dt)
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around")
	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()