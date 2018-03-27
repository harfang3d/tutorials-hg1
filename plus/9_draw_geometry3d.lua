hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(640, 400)

cube = plus:CreateGeometry(plus:CreateCube(0.5, 2, 0.5))

fps = hg.FPSController(0, 2, -10)

while not plus:IsAppEnded() do
	fps:Update(plus:UpdateClock())
	pos, rot = fps:GetPos(), fps:GetRot()
	plus:SetCamera3D(pos.x, pos.y, pos.z, rot.x, rot.y, rot.z)

	plus:Clear()
	for z = -100, 100, 5 do
		for x = -100, 100, 5 do
			plus:Geometry3D(x, 0, z, cube)
		end
	end
	plus:Text2D(5, 5, "Move around with QSZD, left mouse button to look around")
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()