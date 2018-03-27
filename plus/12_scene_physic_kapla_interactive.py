import harfang as hg
from math import pi, cos, sin, asin


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
				world = hg.Matrix4.TransformationMatrix(hg.Vector3(cos(a) * r + x, ring_y, sin(a) * r + z), hg.Vector3(0, -a + y_off, 0))
				tower.append(plus.AddPhysicCube(scn, world, width, height, length, 2)[0])
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


hg.LoadPlugins()

plus = hg.GetPlus()

# initialize rendering
plus.CreateWorkers()
plus.RenderInit(1280, 720)

# create the scene and retrieve its physic system
scn = plus.NewScene()

physic_system = scn.GetPhysicSystem()
physic_system.SetTimestep(1 / 200)  # raise physic frequency for more stability

# create default content
cam = plus.AddCamera(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1, -10)))
plus.AddLight(scn, hg.Matrix4.RotationMatrix(hg.Vector3(0.6, -0.4, 0)), hg.LightModelLinear, 150)
plus.AddLight(scn, hg.Matrix4.RotationMatrix(hg.Vector3(0.6, pi, 0.2)), hg.LightModelLinear, 0, False, hg.Color(0.3, 0.3, 0.4))
plus.AddPhysicPlane(scn)

# create the initial tower
tower_radius = 6
tower_height = 16
nodes = add_kapla_tower(scn, 0.5, 2, 2, tower_radius, tower_height)

# create the FPS controller
fps = hg.FPSController(0, 16, -80)

# enter the simulation loop
while not plus.IsAppEnded():
	# handle inputs
	old_tower_radius, old_tower_height = tower_radius, tower_height

	if plus.KeyPress(hg.KeyF2):
		tower_radius += 1
	elif plus.KeyPress(hg.KeyF1):
		if tower_radius > 5:
			tower_radius -= 1
	elif plus.KeyPress(hg.KeyF4):
		tower_height += 1
	elif plus.KeyPress(hg.KeyF3):
		if tower_height > 1:
			tower_height -= 1

	if tower_radius != old_tower_radius or tower_height != old_tower_height:
		remove_kapla_tower(scn, nodes)
		nodes = add_kapla_tower(scn, 0.5, 2, 2, tower_radius, tower_height)

	if plus.KeyPress(hg.KeySpace):
		world = cam.GetTransform().GetWorld()
		ball, body = plus.AddPhysicSphere(scn, world)
		body.ApplyLinearImpulse(world.GetZ() * 50)
		nodes.append(ball)

	# update the camera controller and synchronize the camera node
	dt = plus.UpdateClock()
	fps.UpdateAndApplyToNode(cam, dt)

	# update scene
	plus.UpdateScene(scn, dt)

	# display on-screen instructions
	plus.Text2D(5, 25, "F1/F2 modify tower radius, F3/F4 modify tower height (%d blocks) @%.2fFPS" % (len(nodes), 1 / hg.time_to_sec_f(dt)))
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around, space to shoot")

	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()
