hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(640, 400)

cube = plus:CreateGeometry(plus:CreateCube(0.5, 2, 0.5))

fps = hg.FPSController(0, 2, -10)
fps:SetRot(hg.Vector3(0.5, 0, 0))

renderer = plus:GetRenderer()
size = plus:GetRenderWindowSize(plus:GetRenderWindow())

function draw_view(viewport, cam_pos, cam_rot)
	renderer:SetViewport(viewport)
	renderer:SetClippingRect(viewport)

	renderer:Clear(hg.Color.Black)

	plus:SetCamera3D(cam_pos.x, cam_pos.y, cam_pos.z, cam_rot.x, cam_rot.y, cam_rot.z)

	for z = -50, 50 - 5, 5 do
		for x = -50, 50 - 5, 5 do
			plus:Geometry3D(x, 0, z, cube)
		end
	end
end

while not plus:IsAppEnded() do
	fps:Update(plus:UpdateClock())

	-- draw the full view at fps position
	pos, rot = fps:GetPos(), fps:GetRot()
	draw_view(hg.Rect(0, 0, size.x, size.y), pos, rot)

	-- process the view on screen
	renderer:DrawFrame()
	plus:Commit2D()
	plus:Commit3D()

	-- draw the vignette on left bottom side with another point of view
	draw_view(hg.Rect(0, 0, size.x * 0.5, size.y * 0.5), pos + hg.Vector3(0, 15, 0), rot)

	plus:Text2D(5, 5, "Move around with QSZD, left mouse button to look around")

	-- send the final rendered image on screen
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()