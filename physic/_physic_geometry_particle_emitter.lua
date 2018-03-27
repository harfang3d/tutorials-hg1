hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:CreateWorkers()
plus:RenderInit(640, 400)

-- create scene
scn = plus:NewScene()
cam = plus:AddCamera(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1, -10)))
plus:AddLight(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(6, 4, -6)))
plus:AddPhysicPlane(scn)

-- layer 1 collides with layer 0 but not with itself
scn:GetPhysicSystem():SetCollisionLayerPairState(0, 1, true)
scn:GetPhysicSystem():SetCollisionLayerPairState(1, 1, false)

-- fps controller to move freely in the scene
fps = hg.FPSController(0, 2, -10)

-- create particles
particle_count = 240
particle_spawn_rate = 60 -- per second
particles = {}

for i = 1, particle_count do
	node, rigid_body = plus:AddPhysicCube(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, -100, 0)), 0.05, 0.05, 0.05)
	-- avoid the particle to collide to each other
	rigid_body:SetCollisionLayer(1)
	-- add to particles
    table.insert(particles, {0, rigid_body})
end

-- update particles life and spawn dead particles
local spawn_rate_control = 0

function update_particles(dt_sec, start_pos, direction)
	-- update particles and get the dead one
	spawn_rate_control = spawn_rate_control - dt_sec

	for i = 1, particle_count do
		local particle = particles[i]

		if particle[1] > 0 then
			particle[1] = particle[1] - dt_sec -- update life
		elseif spawn_rate_control < 0 then
			spawn_rate_control = spawn_rate_control + 1 / particle_spawn_rate

			-- teleport the particle rigid body to its spawn position, wake it up and reset its world matrix
			local rigid_body = particle[2]
			particle[1] = particle_count / particle_spawn_rate

			rigid_body:SetIsSleeping(false)
			rigid_body:ResetWorld(hg.Matrix4.TransformationMatrix(start_pos, hg.Vector3(math.random(0, 100)*0.01, math.random(0, 100)*0.01, math.random(0, 100)*0.01)))
			rigid_body:ApplyLinearImpulse(direction + hg.Vector3(math.random(0, 100)*0.01 * 0.5, math.random(0, 100)*0.01 * 0.5, math.random(0, 100)*0.01 * 0.5))
		end
    end
end

while not plus:IsAppEnded() do
	dt_sec = plus:UpdateClock()

	fps:UpdateAndApplyToNode(cam, dt_sec)

	update_particles(hg.time_to_sec_f(dt_sec), hg.Vector3(2.5, 3, -1), hg.Vector3(-1, 2, 3))

	plus:UpdateScene(scn, dt_sec)
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()