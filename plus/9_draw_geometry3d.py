import gs
import gs.plus.clock as clock
import gs.plus.input as input
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.geometry as geometry

render.init(640, 400, "../pkg.core")

cube = render.create_geometry(geometry.create_cube(0.5, 2, 0.5))

fps = camera.fps_controller(0, 2, -10)

while not input.key_press(gs.InputDevice.KeyEscape):
	fps.update(clock.update())
	render.set_camera3d(fps.pos.x, fps.pos.y, fps.pos.z, fps.rot.x, fps.rot.y, fps.rot.z)

	render.clear()
	for z in range(-100, 100, 5):
		for x in range(-100, 100, 5):
			render.geometry3d(x, 0, z, cube)
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around")
	render.flip()
