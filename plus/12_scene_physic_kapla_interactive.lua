function add_kapla_tower(scn, width, height, length, radius, level_count, x, y, z)
	-- create a Kapla tower, return a list of created nodes
	local tower = {}
	local level_y = y + height / 2

	for i = 0, level_count / 2 - 1 do
		local function fill_ring(r, ring_y, size, r_adjust, y_off)
			local step = math.asin((size * 1.01) / 2 / (r - r_adjust)) * 2
			local cube_count = (2 * math.pi) / step
			local error = 2 * math.pi - step * cube_count
			step = step + error / cube_count -- distribute error

			local a = 0
			while a < (2 * math.pi - error) do
				local world = gs.Matrix4.TransformationMatrix({math.cos(a) * r + x, ring_y, math.sin(a) * r + z}, {0, -a + y_off, 0})
				table.insert(tower, plus:AddPhysicCube(scn, world, width, height, length, 2)[1])
				a = a + step
			end
		end

		fill_ring(radius - length / 2, level_y, width, length / 2, math.pi / 2)
		level_y = level_y + height
		fill_ring(radius - length + width / 2, level_y, length, width / 2, 0)
		fill_ring(radius - width / 2, level_y, length, width / 2, 0)
		level_y = level_y + height
	end

	return tower
end

function remove_kapla_tower(scn, tower)
	-- remove all nodes in a Kapla tower from the scene
	for i, node in pairs(tower) do
		scn:RemoveNode(node)
	end
end

gs.LoadPlugins()

plus = gs.GetPlus()

-- initialize rendering
plus:CreateWorkers()
plus:RenderInit(1280, 720)

-- create the scene and retrieve its physic system
scn = plus:NewScene()

physic_system = scn:GetSystem("Physic")
physic_system:SetTimestep(1 / 200) -- raise physic frequency for more stability

-- create default content
cam = plus:AddCamera(scn, gs.Matrix4.TranslationMatrix({0, 1, -10}))
plus:AddLight(scn, gs.Matrix4.RotationMatrix({0.6, -0.4, 0}), gs.Light.Model_Linear, 150)
plus:AddLight(scn, gs.Matrix4.RotationMatrix({0.6, math.pi, 0.2}), gs.Light.Model_Linear, 0, false, {0.3, 0.3, 0.4})
plus:AddPhysicPlane(scn)

-- create the initial tower
tower_radius = 6
tower_height = 16
nodes = add_kapla_tower(scn, 0.5, 2, 2, tower_radius, tower_height, 0, 0, 0)

-- create the FPS controller
fps = gs.FPSController(0, 16, -80)

-- enter the simulation loop
while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	-- handle inputs
	local old_tower_radius, old_tower_height = tower_radius, tower_height

	if plus:KeyPress(gs.InputDevice.KeyF2) then
		tower_radius = tower_radius + 1
	elseif plus:KeyPress(gs.InputDevice.KeyF1) then
		if tower_radius > 5 then
			tower_radius = tower_radius - 1
		end
	elseif plus:KeyPress(gs.InputDevice.KeyF4) then
		tower_height = tower_height + 1
	elseif plus:KeyPress(gs.InputDevice.KeyF3) then
		if tower_height > 1 then
			tower_height = tower_height - 1
		end
	end

	if tower_radius ~= old_tower_radius or tower_height ~= old_tower_height then
		remove_kapla_tower(scn, nodes)
		nodes = add_kapla_tower(scn, 0.5, 2, 2, tower_radius, tower_height, 0, 0, 0)
	end

	if plus:KeyPress(gs.InputDevice.KeySpace) then
		world = cam:GetTransform():GetWorld()
		ball, body = plus:AddPhysicSphere(scn, world)
		body:ApplyLinearImpulse(world:GetZ() * 50)
		table.insert(nodes, ball)
	end

	-- update the camera controller and synchronize the camera node
	dt = plus:UpdateClock()
	fps:UpdateAndApplyToNode(cam, dt)

	-- update scene
	plus:UpdateScene(scn, dt)

	-- display on-screen instructions
	plus:Text2D(5, 25, string.format("F1/F2 modify tower radius, F3/F4 modify tower height (%d blocks) @%.2fFPS", #nodes, 1 / dt:to_sec()))
	plus:Text2D(5, 5, "Move around with QSZD, left mouse button to look around, space to shoot")

	plus:Flip()
end
