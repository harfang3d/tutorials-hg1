-- path finding sample, left click to change start point, right click to change end point.

gs.LoadPlugins()

plus = gs.GetPlus()
plus:RenderInit(1280, 720, 8)

gs.MountFileDriver(gs.StdFileDriver("../_data/"))

-- setup scene
scn = plus:NewScene(false, false)
plus:AddEnvironment(scn, gs.Color.Black, gs.Color(0.25, 0.25, 0.3))

cam = plus:AddCamera(scn, gs.Matrix4.TransformationMatrix({0, 65, -55}, {0.9, 0, 0}))
lgt = plus:AddLight(scn, gs.Matrix4.TransformationMatrix({40, 50, -60}, {0.75, -0.6, 0}), gs.Light.Model_Spot)
lgt:GetLight():SetConeAngle(0.49)
lgt:GetLight():SetEdgeAngle(0.1)

gfx = gs.SimpleGraphicSceneOverlay(false)
scn:AddComponent(gfx)

-- create the navigation system and component
nav_sys = scn:AddSystem(gs.NavigationSystem())
nav_sys:SetDebugVisuals(false)

geo = gs.LoadCoreGeometry("maze/maze.geo")
nav_geo = gs.CreateNavigationGeometry(geo, nav_sys:GetConfig())

nav = gs.Navigation()
nav:SetGeometry(nav_geo)

maze = plus:AddGeometry(scn, "maze/maze.geo")
maze:AddComponent(nav)

-- main loop
path = gs.NavigationPath()
start, endpoint = gs.Vector3(2, 1, -23), gs.Vector3(-3, 1, 23)

font = gs.RasterFont("@core/fonts/default.ttf", 32)

picker = gs.ScenePicking(plus:GetRenderSystem())

while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	nav:FindPathTo(start, endpoint, path)

	plus:UpdateScene(scn, gs.time(0))

	-- pick start/end points
	if picker:Prepare(scn, false, true):get() == true then
		local mx, my = plus:GetMousePos()
		if plus:MouseButtonDown(gs.InputDevice.Button0) then
			result, start = picker:PickWorld(scn, mx, my)
		elseif plus:MouseButtonDown(gs.InputDevice.Button1) then
			result, endpoint = picker:PickWorld(scn, mx, my)
		end
	end

	-- display current path
	points = path:GetPoints()
	for i = 1, #points - 1 do
		local a, b = points[i], points[i + 1]
		gfx:Line(a.x, a.y, a.z, b.x, b.y, b.z, gs.Color.Yellow, gs.Color.Yellow)
	end

	-- label start/end points
	gfx:SetDepthTest(false)
	gfx:SetBlendMode(gs.BlendAlpha)
	gfx:Text(start.x, start.y, start.z, ".Start", gs.Color.White, font, 0.05)
	gfx:Text(endpoint.x, endpoint.y, endpoint.z, ".End", gs.Color.White, font, 0.05)
	gfx:SetBlendMode(gs.BlendOpaque)
	gfx:SetDepthTest(true)

	plus:Flip()
end
