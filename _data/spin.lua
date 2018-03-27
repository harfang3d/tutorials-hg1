function Update()
	local rot = this:GetTransform():GetRotation()
	rot.x = rot.x + engine.dt * 1.5
	rot.z = rot.z + engine.dt
	this:GetTransform():SetRotation(rot)
end
