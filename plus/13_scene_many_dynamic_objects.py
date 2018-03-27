import harfang as hg
from math import cos, sin

hg.LoadPlugins()

plus = hg.GetPlus()

plus.CreateWorkers()
plus.RenderInit(1280, 720)

scn = plus.NewScene()
cam = plus.AddCamera(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1, -10)))
plus.AddLight(scn, hg.Matrix4.RotationMatrix(hg.Vector3(0.6, -0.4, 0)), hg.LightModelLinear, 100, False)
plus.AddPlane(scn)

fps = hg.FPSController(0, 16, -80)

rows = []
for z in range(-200, 200, 2):
	row = []
	for x in range(-200, 200, 2):
		pos = hg.Vector3(x, 1, z)
		node = plus.AddCube(scn, hg.Matrix4.TranslationMatrix(pos), 1, 12, 1)
		row.append((node, pos))
	rows.append(row)

angle, animate = 0, True
while not plus.IsAppEnded():
	dt = plus.UpdateClock()
	fps.UpdateAndApplyToNode(cam, dt)

	scn.Update(dt)

	# NOTE: Here we break out of the high-level scene.Update call in order to
	# take profit of multiple core and run the following script code while the
	# scene systems are updating.
	# You can move the WaitUpdate(True) above this command to see the effect on
	# performance of updating the scene and its content sequencially.
	if plus.KeyPress(hg.KeySpace):
		animate = not animate

	if animate:
		for j, row in enumerate(rows):
			crow = cos(angle + j * 0.1)
			for i, node_pos in enumerate(row):
				node_pos[1].y = crow * sin(angle + i * 0.1) * 6 + 6.5
				node_pos[0].GetTransform().SetPosition(node_pos[1])
		angle += hg.time_to_sec_f(dt)

	scn.WaitUpdate(True)  # move this call right after the Update call to reduce performance
	scn.Commit()
	scn.WaitCommit(True)

	plus.Text2D(5, 25, "40000 dynamic objects @%.2fFPS" % (1 / hg.time_to_sec_f(dt)))
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around, space to toggle script animation")
	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()