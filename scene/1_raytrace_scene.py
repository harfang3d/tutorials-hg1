# Raytrace through a physic scene
import gs

gs.LoadPlugins()

plus = gs.GetPlus()
plus.RenderInit(1024, 768)

scn = plus.NewScene(True)

cam = plus.AddCamera(scn, gs.Matrix4.TranslationMatrix((0, 0, -3)))
plus.AddLight(scn, gs.Matrix4.TranslationMatrix((0, 7, 0)), gs.Light.Model_Linear)
plus.AddPlane(scn)

cube, cube_body = plus.AddPhysicCube(scn, gs.Matrix4.Identity, 1, 1, 1, 0)
cube_body.SetType(gs.RigidBodyKinematic)

gfx = gs.SimpleGraphicSceneOverlay(False)
scn.AddComponent(gfx)

cube_angle = 0
while not plus.KeyPress(gs.InputDevice.KeyEscape):
	dt = plus.UpdateClock()

	cube.GetTransform().SetRotation(gs.Vector3(cube_angle, cube_angle * 2, 0))
	cube_angle += 0.01

	# launch front direction from the camera and see if I hit the cube
	world = cam.GetTransform().GetWorld()
	dir, dir_x, dir_y, pos = world.GetZ(), world.GetX(), world.GetY(), world.GetTranslation()

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

	plus.UpdateScene(scn, dt)
	plus.Flip()
