function Update()
	-- spin
	local rot = this:GetTransform():GetRotation()
	rot.z = rot.z + engine.dt
	this:GetTransform():SetRotation(rot)

	-- sleep
	hg.Sleep(hg.time_from_ms(500)) -- in ms
end
