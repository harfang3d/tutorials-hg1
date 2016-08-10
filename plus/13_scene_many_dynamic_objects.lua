plus = gs.GetPlus()

plus:CreateWorkers()
plus:RenderInit(1280, 720)

scn = plus:NewScene()
cam = plus:AddCamera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
plus:AddLight(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 100, false)
plus:AddPlane(scn)

fps = gs.FPSController(0, 16, -80)

rows = {}
for z = -200, 200-2, 2 do
	local row = {}
	for x = -200, 200-2, 2 do
		local pos = gs.Vector3(x, 1, z)
		local node = plus:AddCube(scn, gs.Matrix4.TranslationMatrix(pos), 1, 12, 1)
		table.insert(row, {node, pos})
	end
	table.insert(rows, row)
end

angle, animate = 0, true
while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	local dt = plus:UpdateClock()
	fps:UpdateAndApplyToNode(cam, dt)

	scn:Update(dt)

	-- NOTE: Here we break out of the high-level scene.Update call in order to
	-- take profit of multiple core and run the following script code while the
	-- scene systems are updating.
	-- You can move the WaitUpdate(True) above this command to see the effect on
	-- performance of updating the scene and its content sequencially.
	if plus:KeyPress(gs.InputDevice.KeySpace) then
		animate = not animate
	end

	if animate then
		for j = 1, #rows do
			local row = rows[j]
			local crow = math.cos(angle + j * 0.1)
			for i = 1, #row do
				local node_pos = row[i]
				node_pos[2].y = crow * math.sin(angle + i * 0.1) * 6 + 6.5
				node_pos[1]:GetTransform():SetPosition(node_pos[2])
			end
		end
		angle = angle + dt:to_sec()
	end

	scn:WaitUpdate(true) -- move this call right after the Update call to reduce performance
	scn:Commit()
	scn:WaitCommit(true)

	plus:Text2D(5, 25, string.format("40000 dynamic objects @%.2fFPS", 1 / dt:to_sec()))
	plus:Text2D(5, 5, "Move around with QSZD, left mouse button to look around, space to toggle script animation")
	plus:Flip()
end
