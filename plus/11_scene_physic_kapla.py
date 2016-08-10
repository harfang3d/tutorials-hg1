import gs
from math import pi, cos, sin, asin


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
				world = gs.Matrix4.TransformationMatrix((cos(a) * r + x, ring_y, sin(a) * r + z), (0, -a + y_off, 0))
				plus.AddPhysicCube(scn, world, width, height, length, 2)
				a += step

		fill_ring(radius - length / 2, level_y, width, length / 2, pi / 2)
		level_y += height
		fill_ring(radius - length + width / 2, level_y, length, width / 2, 0)
		fill_ring(radius - width / 2, level_y, length, width / 2, 0)
		level_y += height


gs.LoadPlugins()

plus = gs.GetPlus()

plus.CreateWorkers()
plus.RenderInit(640, 400)

scn = plus.NewScene()

cam = plus.AddCamera(scn, gs.Matrix4.TranslationMatrix((0, 1, -10)))
plus.AddLight(scn, gs.Matrix4.RotationMatrix((0.6, -0.4, 0)), gs.Light.Model_Linear, 150)
plus.AddLight(scn, gs.Matrix4.RotationMatrix((0.6, pi, 0.2)), gs.Light.Model_Linear, 0, True, (0.3, 0.3, 0.4))
plus.AddPhysicPlane(scn)

nodes = add_kapla_tower(scn, 0.5, 2, 2, 6, 16)

fps = gs.FPSController(0, 16, -80)

while not plus.KeyPress(gs.InputDevice.KeyEscape):
	dt = plus.UpdateClock()
	fps.UpdateAndApplyToNode(cam, dt)

	plus.UpdateScene(scn, dt)

	plus.Text2D(5, 25, "@%.2fFPS" % (1 / dt.to_sec()))
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around")
	plus.Flip()
