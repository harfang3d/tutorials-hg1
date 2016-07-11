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
	tower = []
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
				tower.append(scene.add_physic_cube(scn, world, width, height, length, 2)[0])
				a += step

		fill_ring(radius - length / 2, level_y, width, length / 2, pi / 2)
		level_y += height
		fill_ring(radius - length + width / 2, level_y, length, width / 2, 0)
		fill_ring(radius - width / 2, level_y, length, width / 2, 0)
		level_y += height

	return tower


def remove_kapla_tower(scn, tower):
	"""Remove all nodes in a Kapla tower from the scene"""
	for node in tower:
		scn.RemoveNode(node)


# start worker threads
gs.plus.create_workers()

# initialize rendering
render.init(1280, 720, "../pkg.core")

# create the scene and retrieve its physic system
scn = scene.new_scene()

physic_system = scn.GetSystem("Physic")
physic_system.SetTimestep(1 / 200)  # raise physic frequency for more stability

# create default content
cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 150)
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, pi, 0.2)), gs.Light.Model_Linear, diffuse=gs.Color(0.3, 0.3, 0.4), shadow=False)
scene.add_physic_plane(scn)

# create the initial tower
tower_radius = 6
tower_height = 16
nodes = add_kapla_tower(scn, 0.5, 2, 2, tower_radius, tower_height)

# create the FPS controller
fps = camera.fps_controller(0, 16, -80)

# enter the simulation loop
while not input.key_press(gs.InputDevice.KeyEscape):
	# handle inputs
	old_tower_radius = tower_radius

	if input.key_press(gs.InputDevice.KeyF2):
		tower_radius += 1
	elif input.key_press(gs.InputDevice.KeyF1):
		if tower_radius > 5:
			tower_radius -= 1
	elif input.key_press(gs.InputDevice.KeyF4):
		tower_height += 1
	elif input.key_press(gs.InputDevice.KeyF3):
		if tower_height > 1:
			tower_height -= 1

	if tower_radius != old_tower_radius:
		remove_kapla_tower(scn, nodes)
		nodes = add_kapla_tower(scn, 0.5, 2, 2, tower_radius, tower_height)

	if input.key_press(gs.InputDevice.KeySpace):
		world = cam.GetTransform().GetWorld()
		ball, rigid_body = scene.add_physic_sphere(scn, world)
		rigid_body.ApplyLinearImpulse(world.GetZ() * 50)
		nodes.append(ball)

	# update the camera controller and synchronize the camera node
	dt_sec = clock.update()
	fps.update_and_apply_to_node(cam, dt_sec)

	# update scene
	scene.update_scene(scn, dt_sec)

	# display on-screen instructions
	render.text2d(5, 25, "F1/F2 modify tower radius, F3/F4 modify tower height (%d blocks) @%.2fFPS" % (len(nodes), 1 / dt_sec))
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around, space to shoot")

	render.flip()
