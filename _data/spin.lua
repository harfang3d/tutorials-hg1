execution_context = gs.ScriptContextAll

function Update()
	local rot = this:GetTransform():GetRotation()
	rot.x = rot.x + engine:GetClockDelta() * 1.5
	rot.z = rot.z + engine:GetClockDelta()
	this:GetTransform():SetRotation(rot)
end
