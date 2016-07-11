# Display a terrain scene with light atmospheric features

import os
import gs
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.scene as scene
import gs.plus.clock as clock

gs.LoadPlugins(gs.get_default_plugins_path())

# mount data folder
pic = gs.MountFileDriver(gs.StdFileDriver(os.path.join(os.getcwd(), "../_data")), "@data")

# create the renderer
render.init(1280, 720, "../pkg.core", 4)

# create scene
scn = scene.new_scene(False, True)
scene.add_environment(scn, gs.Color.Black, gs.Color.Black, gs.Color(0.85, 0.9, 1), 8000, 60000)

# fps camera
cam = scene.add_camera(scn)
cam.GetCamera().SetZNear(1)
cam.GetCamera().SetZFar(100000)  # 100km
fps = camera.fps_controller(0, 3000, -30000, 10, 100)

# sky lighting
sky = gs.RenderScript()
sky.SetPath("@core/lua/sky_lighting.lua")
sky.Set("time_of_day", 16.5)
sky.Set("attenuation", 0.75)
sky.Set("shadow_range", 10000.0)  # 10km shadow range
sky.Set("shadow_split", gs.Vector4(0.1, 0.2, 0.3, 0.4))
scn.AddComponent(sky)

# load terrain
terrain = gs.Terrain()
terrain.SetSize(gs.Vector3(68767, 5760, 68767))
terrain.SetHeightmap("@data/terrain/island.r16")
terrain.SetHeightmapResolution(gs.iVector2(1024, 1024))
terrain.SetMinPrecision(50)  # don't bother with a very fine grid given the low resolution heightmap in use
terrain.SetSurfaceShader("@data/terrain/island.isl")

terrain_node = gs.Node()
terrain_node.AddComponent(gs.Transform())
terrain_node.AddComponent(terrain)
scn.AddNode(terrain_node)

#
while True:
	dt = clock.get_dt()

	old_pos = gs.Vector3(fps.pos)
	fps.update_and_apply_to_node(cam, dt)
	speed = gs.Vector3.Dist(fps.pos, old_pos) / dt if dt > 0 else 0

	scene.update_scene(scn, dt)

	render.text2d(5, 25, "Current speed: %d m/s" % int(speed))
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around (hold shift to go faster)")
	render.flip()

	clock.update()

