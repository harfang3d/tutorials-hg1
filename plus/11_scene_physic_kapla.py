import gs
import gs.plus
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock
from math import pi, cos, sin, asin

gs.LoadPlugins(gs.get_default_plugins_path())


def add_kapla_tower(scn, width, height, length, radius, level_count: int, x=0, y=0, z=0):
	"""Create a Kapla tower, return a list of created nodes"""
	level_y = y + height / 2

	for i in range(level_count // 2):
		def fill_ring(r, ring_y, size, r_adjust, y_off):
			step = asin((size * 1.01) / 2 / (r - r_adjust)) * 2
			cube_count = (2 * pi) // step
			error = 2 * pi - step * cube_count
			step += error / cube_count  # distribute error

			a = 0
			while a < (2 * pi - error):
				world = gs.Matrix4.TransformationMatrix(gs.Vector3(cos(a) * r + x, ring_y, sin(a) * r + z), gs.Vector3(0, -a + y_off, 0))
				scene.add_physic_cube(scn, world, width, height, length, 2)
				a += step

		fill_ring(radius - length / 2, level_y, width, length / 2, pi / 2)
		level_y += height
		fill_ring(radius - length + width / 2, level_y, length, width / 2, 0)
		fill_ring(radius - width / 2, level_y, length, width / 2, 0)
		level_y += height


gs.plus.create_workers()

render.init(1280, 720, "../pkg.core")

scn = scene.new_scene()

cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 150)
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, pi, 0.2)), gs.Light.Model_Linear, diffuse=gs.Color(0.3, 0.3, 0.4))
scene.add_physic_plane(scn)

nodes = add_kapla_tower(scn, 0.5, 2, 2, 6, 16)

fps = camera.fps_controller(0, 16, -80)

while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()
	fps.update_and_apply_to_node(cam, dt_sec)

	scene.update_scene(scn, dt_sec)

	render.text2d(5, 25, "@%.2fFPS" % (1 / dt_sec))
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around")
	render.flip()
