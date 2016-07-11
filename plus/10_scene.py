import gs
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock

render.init(640, 400, "../pkg.core")

scn = scene.new_scene()

cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
scene.add_light(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(6, 4, -6)))
scene.add_cube(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0.5, 0)))
scene.add_plane(scn)

fps = camera.fps_controller(0, 2, -10)

while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()

	fps.update_and_apply_to_node(cam, dt_sec)

	scene.update_scene(scn, dt_sec)
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around")
	render.flip()
