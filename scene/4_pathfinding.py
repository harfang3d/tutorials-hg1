# path finding sample, left click to change start point, right click to change end point.
import harfang as hg

hg.LoadPlugins()

hg.MountFileDriver(hg.StdFileDriver("_data/"))

resolution = hg.Vector2(1280, 720)
antialiasing = 4

plus = hg.GetPlus()
plus.RenderInit(int(resolution.x), int(resolution.y), antialiasing)

# setup scene
scn = plus.NewScene(False, False)

plus.AddEnvironment(scn,hg.Color.Black, hg.Color(0.25, 0.25, 0.3))

cam = plus.AddCamera(scn, hg.Matrix4.TransformationMatrix(hg.Vector3(0, 65, -55), hg.Vector3(0.9, 0, 0)))
lgt = plus.AddLight(scn, hg.Matrix4.TransformationMatrix(hg.Vector3(40, 50, -60), hg.Vector3(0.75, -0.6, 0)), hg.LightModelSpot)
lgt.GetLight().SetConeAngle(0.49)
lgt.GetLight().SetEdgeAngle(0.1)

gfx = hg.SimpleGraphicSceneOverlay(False)
scn.AddComponent(gfx)

# create the navigation system and component
nav_sys = hg.NavigationSystem()
nav_sys.SetDebugVisuals(False)
scn.AddSystem(nav_sys)

geo = hg.LoadGeometry("maze/maze.geo")
nav_geo = hg.CreateNavigationGeometry(geo, nav_sys.GetConfig())

nav = hg.Navigation()
nav.SetGeometry(nav_geo)

maze = plus.AddGeometry(scn, "maze/maze.geo")
maze.AddComponent(nav)

# main loop
start, endpoint = hg.Vector3(2, 1, -23), hg.Vector3(-3, 1, 23)

font = hg.RasterFont("@core/fonts/default.ttf", 32)

picker = hg.ScenePicking(plus.GetRenderSystem())

while not plus.IsAppEnded():
	ok, path = nav.FindPathTo(start, endpoint)
	dt = plus.UpdateClock()
	plus.UpdateScene(scn, dt)

	# pick start/end points
	if picker.Prepare(scn, False, True).get():
		mx, my = plus.GetMousePos()
		my = resolution.y - my
		if plus.MouseButtonDown(hg.Button0):
			result, start = picker.PickWorld(scn, mx, my)
		elif plus.MouseButtonDown(hg.Button1):
			result, endpoint = picker.PickWorld(scn, mx, my)
	
	# display current path
	if ok:
		for i in range(1, path.point.size()):
			a, b = path.point.at(i-1), path.point.at(i)
			gfx.Line(a.x, a.y, a.z, b.x, b.y, b.z, hg.Color.Yellow, hg.Color.Yellow)
	
	# label start/end points
	gfx.SetDepthTest(False)
	gfx.SetBlendMode(hg.BlendAlpha)
	gfx.Text(start.x, start.y, start.z, ".Start", hg.Color.White, font, 0.05)
	gfx.Text(endpoint.x, endpoint.y, endpoint.z, ".End", hg.Color.White, font, 0.05)
	gfx.SetBlendMode(hg.BlendOpaque)
	gfx.SetDepthTest(True)

	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()