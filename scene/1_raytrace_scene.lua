-- Raytrace through a physic scene
hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(1024, 768)

scn = plus:NewScene(true)

cam = plus:AddCamera(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 0, -3)))
plus:AddLight(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 7, 0)), hg.LightModelLinear)
plus:AddPlane(scn)

cube, cube_body = plus:AddPhysicCube(scn, hg.Matrix4.Identity, 1, 1, 1, 0)
cube_body:SetType(hg.RigidBodyKinematic)

gfx = hg.SimpleGraphicSceneOverlay(false)
scn:AddComponent(gfx)

cube_angle = 0
while not plus:IsAppEnded() do
	local dt = plus:UpdateClock()

	cube:GetTransform():SetRotation(hg.Vector3(cube_angle, cube_angle * 2, 0))
	cube_angle = cube_angle + 0.01

	-- launch front direction from the camera and see if I hit the cube
	local world = cam:GetTransform():GetWorld()
	local dir, dir_x, dir_y, pos = world:GetZ(), world:GetX(), world:GetY(), world:GetTranslation()

	local function draw_cross(p)
		local k = 0.01
		gfx:Line(p.x, p.y, p.z, p.x - k, p.y, p.z, hg.Color.White, hg.Color.Red)
		gfx:Line(p.x, p.y, p.z, p.x + k, p.y, p.z, hg.Color.White, hg.Color.Red)
		gfx:Line(p.x, p.y, p.z, p.x, p.y - k, p.z, hg.Color.White, hg.Color.Red)
		gfx:Line(p.x, p.y, p.z, p.x, p.y + k, p.z, hg.Color.White, hg.Color.Red)
	end

	for i = -20, 20 - 1 do
		for j = -20, 20 - 1 do
			local has_hit, hit = scn:GetPhysicSystem():Raycast(pos, (dir + dir_x * i * 0.01 + dir_y * j * 0.01):Normalized())
			if has_hit then
				draw_cross(hit:GetPosition())
			end
		end
	end

	plus:UpdateScene(scn, dt)
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()
