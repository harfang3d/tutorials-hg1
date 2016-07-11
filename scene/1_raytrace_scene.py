# Raytrace through a physic scene
import gs
import gs.plus.render as render
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock

gs.LoadPlugins(gs.get_default_plugins_path())

render.init(1024, 768, "../pkg.core")

scn = scene.new_scene(True)

cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0, -3)))
scene.add_light(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 7, 0)), gs.Light.Model_Linear)
scene.add_plane(scn)

cube, cube_body = scene.add_physic_cube(scn, mass=0)
cube_body.SetType(gs.RigidBodyKinematic)

gfx = gs.SimpleGraphicSceneOverlay(False)
scn.AddComponent(gfx)

cube_angle = 0
while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()

	cube.GetTransform().SetRotation(gs.Vector3(cube_angle, cube_angle*2, 0))
	cube_angle += 0.01

	# launch front direction from the camera and see if I hit the cube
	world = cam.GetTransform().GetWorld()
	dir = world.GetZ()
	dir_x = world.GetX()
	dir_y = world.GetY()
	pos = world.GetTranslation()

	def draw_cross(p):
		k = 0.01
		gfx.Line(p.x, p.y, p.z, p.x - k, p.y, p.z, gs.Color.White, gs.Color.Red)
		gfx.Line(p.x, p.y, p.z, p.x + k, p.y, p.z, gs.Color.White, gs.Color.Red)
		gfx.Line(p.x, p.y, p.z, p.x, p.y - k, p.z, gs.Color.White, gs.Color.Red)
		gfx.Line(p.x, p.y, p.z, p.x, p.y + k, p.z, gs.Color.White, gs.Color.Red)

	for i in range(-20, 20):
		for j in range(-20, 20):
			has_hit, hit = scn.GetSystem("Physic").Raycast(pos, (dir + dir_x * i * 0.01 + dir_y * j * 0.01).Normalized())
			if has_hit:
				draw_cross(hit.GetPosition())

	scene.update_scene(scn, dt_sec)
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around")
	render.flip()
