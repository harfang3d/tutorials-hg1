function Update()
	local rot = this:GetTransform():GetRotation()
	rot.x = rot.x + engine:GetClockDt() * 1.5
	rot.z = rot.z + engine:GetClockDt()
	this:GetTransform():SetRotation(rot)
end
