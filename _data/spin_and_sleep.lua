execution_context = gs.ScriptContextAll

function Update()
	-- spin
	local rot = this:GetTransform():GetRotation()
	rot.z = rot.z + engine:GetClockDelta()
	this:GetTransform():SetRotation(rot)

	-- sleep
	gs.Sleep(500) -- in ms
end
