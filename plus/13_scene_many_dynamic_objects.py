import gs
import gs.plus
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock
from math import cos, sin

gs.plus.create_workers()

render.init(1280, 720, "../pkg.core")

scn = scene.new_scene()
cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 100, shadow=False)
scene.add_plane(scn)

fps = camera.fps_controller(0, 16, -80)

rows = []
for z in range(-200, 200, 2):
	row = []
	for x in range(-200, 200, 2):
		pos = gs.Vector3(x, 1, z)
		node = scene.add_cube(scn, gs.Matrix4.TranslationMatrix(pos), 1, 12, 1)
		row.append((node, pos))
	rows.append(row)

angle, animate = 0, True
while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()
	fps.update_and_apply_to_node(cam, dt_sec)

	scn.Update(gs.time(dt_sec))

	# NOTE: Here we break out of the high-level scene.Update call in order to
	# take profit of multiple core and run the following Python code while the
	# scene systems are updating.
	# You can move the WaitUpdate(True) above this command to see the effect on
	# performance of updating the scene and its content sequentially.
	if input.key_press(gs.InputDevice.KeySpace):
		animate = not animate

	if animate:
		for j, row in enumerate(rows):
			crow = cos(angle + j * 0.1)
			for i, node_pos in enumerate(row):
				node_pos[1].y = crow * sin(angle + i * 0.1) * 6 + 6.5
				node_pos[0].GetTransform().SetPosition(node_pos[1])
		angle += clock.get_dt()

	scn.WaitUpdate(True)  # move this call right after the Update call to reduce performance
	scn.Commit()
	scn.WaitCommit(True)

	render.text2d(5, 25, "40000 dynamic objects @%.2fFPS" % (1 / dt_sec))
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around, space to toggle Python animation")
	render.flip()
