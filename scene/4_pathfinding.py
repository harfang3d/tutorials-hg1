# Path finding sample, left click to change start point, right click to change end point.

import gs
import gs.plus.render as render
import gs.plus.input as input
import gs.plus.scene as scene

gs.LoadPlugins(gs.get_default_plugins_path())
width, height = 1280, 720
render.init(width, height, "../pkg.core", 8)

gs.MountFileDriver(gs.StdFileDriver("../_data/"))

# setup scene
scn = scene.new_scene(False, False)
scene.add_environment(scn, ambient_color=gs.Color(0.25, 0.25, 0.3))

cam = scene.add_camera(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(0, 65, -55), gs.Vector3(0.9, 0, 0)))
lgt = scene.add_light(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(40, 50, -60), gs.Vector3(0.75, -0.6, 0)), gs.Light.Model_Spot)
lgt.GetLight().SetConeAngle(0.49)
lgt.GetLight().SetEdgeAngle(0.1)

gfx = gs.SimpleGraphicSceneOverlay(False)
scn.AddComponent(gfx)

# create the navigation system and component
nav_sys = scn.AddSystem(gs.NavigationSystem())
nav_sys.SetDebugVisuals(False)

geo = gs.LoadCoreGeometry("maze/maze.geo")
nav_geo = gs.CreateNavigationGeometry(geo, nav_sys.GetConfig())

nav = gs.Navigation()
nav.SetGeometry(nav_geo)

maze = scene.add_geometry(scn, "maze/maze.geo")
maze.AddComponent(nav)

# main loop
path = gs.NavigationPath()
start, end = gs.Vector3(2, 1, -23), gs.Vector3(-3, 1, 23)

font = gs.RasterFont("@core/fonts/default.ttf", 32)

picker = gs.ScenePicking(render.get_render_system())

while not input.key_press(gs.InputDevice.KeyEscape):
	nav.FindPathTo(start, end, path)

	scene.update_scene(scn, 1 / 60)

	# pick start/end points
	if picker.Prepare(scn, False, True).get() == True:
		mx, my = input.get_mouse_pos()
		if input.mouse_button_down(gs.InputDevice.Button0):
			result, start = picker.PickWorld(scn, mx, my)
		elif input.mouse_button_down(gs.InputDevice.Button1):
			result, end = picker.PickWorld(scn, mx, my)

	# display current path
	points = path.GetPoints()
	for i in range(len(points)-1):
		a, b = points[i], points[i + 1]
		gfx.Line(a.x, a.y, a.z, b.x, b.y, b.z, gs.Color.Yellow, gs.Color.Yellow)

	# label start/end points
	gfx.SetDepthTest(False)
	gfx.SetBlendMode(gs.BlendAlpha)
	gfx.Text(start.x, start.y, start.z, ".Start", gs.Color.White, font, 0.05)
	gfx.Text(end.x, end.y, end.z, ".End", gs.Color.White, font, 0.05)
	gfx.SetBlendMode(gs.BlendOpaque)
	gfx.SetDepthTest(True)

	render.flip()
