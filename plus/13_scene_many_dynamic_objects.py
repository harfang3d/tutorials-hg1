import gs
from math import cos, sin

plus = gs.GetPlus()

plus.CreateWorkers()
plus.RenderInit(1280, 720)

scn = plus.NewScene()
cam = plus.AddCamera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
plus.AddLight(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 100, False)
plus.AddPlane(scn)

fps = gs.FPSController(0, 16, -80)

rows = []
for z in range(-200, 200, 2):
	row = []
	for x in range(-200, 200, 2):
		pos = gs.Vector3(x, 1, z)
		node = plus.AddCube(scn, gs.Matrix4.TranslationMatrix(pos), 1, 12, 1)
		row.append((node, pos))
	rows.append(row)

angle, animate = 0, True
while not plus.KeyPress(gs.InputDevice.KeyEscape):
	dt = plus.UpdateClock()
	fps.UpdateAndApplyToNode(cam, dt)

	scn.Update(dt)

	# NOTE: Here we break out of the high-level scene.Update call in order to
	# take profit of multiple core and run the following script code while the
	# scene systems are updating.
	# You can move the WaitUpdate(True) above this command to see the effect on
	# performance of updating the scene and its content sequencially.
	if plus.KeyPress(gs.InputDevice.KeySpace):
		animate = not animate

	if animate:
		for j, row in enumerate(rows):
			crow = cos(angle + j * 0.1)
			for i, node_pos in enumerate(row):
				node_pos[1].y = crow * sin(angle + i * 0.1) * 6 + 6.5
				node_pos[0].GetTransform().SetPosition(node_pos[1])
		angle += dt.to_sec()

	scn.WaitUpdate(True)  # move this call right after the Update call to reduce performance
	scn.Commit()
	scn.WaitCommit(True)

	plus.Text2D(5, 25, "40000 dynamic objects @%.2fFPS" % (1 / dt.to_sec()))
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around, space to toggle script animation")
	plus.Flip()
