-- display a terrain scene with light atmospheric features

hg = require("harfang")

hg.LoadPlugins()

-- mount data folder
hg.MountFileDriver(hg.StdFileDriver("_data"), "@data")

-- create the renderer
plus = hg.GetPlus()
plus:RenderInit(1280, 720, 4)

-- create scene
scn = plus:NewScene(false, true)
plus:AddEnvironment(scn, hg.Color.Black, hg.Color.Black, hg.Color(0.85, 0.9, 1), 8000, 60000)

-- camera
cam = plus:AddCamera(scn)
cam:GetCamera():SetZNear(1)
cam:GetCamera():SetZFar(100000) -- 100km

-- sky lighting
sky = hg.RenderScript("@core/lua/sky_lighting.lua")
sky:Set("time_of_day", 16.5)
sky:Set("attenuation", 0.75)
sky:Set("shadow_range", 10000.0) -- 10km shadow range
sky:Set("shadow_split", hg.Vector4(0.1, 0.2, 0.3, 0.4))
scn:AddComponent(sky)

-- load terrain
terrain = hg.Terrain()
terrain:SetSize(hg.Vector3(68767, 5760, 68767))
terrain:SetHeightmap("@data/terrain/island.r16")
terrain:SetHeightmapResolution(hg.IntVector2(1024, 1024))
terrain:SetMinPrecision(50) -- don't bother with a very fine grid given the low resolution heightmap in use
terrain:SetSurfaceShader("@data/terrain/island.isl")

terrain_node = hg.Node()
terrain_node:AddComponent(hg.Transform())
terrain_node:AddComponent(terrain)
scn:AddNode(terrain_node)

--
fps = hg.FPSController(0, 3000, -30000, 10, 100)

while not plus:IsAppEnded() do
	local dt = plus:UpdateClock()

	local old_pos = fps:GetPos()
	fps:UpdateAndApplyToNode(cam, dt)
	speed = dt > 0 and hg.Dist(fps:GetPos(), old_pos) / hg.time_to_sec_f(dt) or 0
		
	plus:UpdateScene(scn, dt)

	plus:Text2D(5, 25, string.format("Current speed: %d m/s", math.floor(speed)))
	plus:Text2D(5, 5, "Move around with QSZD, left mouse button to look around (hold shift to go faster)")
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()
