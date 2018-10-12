-- How to draw a picture on a primitive

hg = require("harfang")

-- load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

-- create the renderer
renderer = hg.CreateRenderer()
renderer:Open()

-- open a new window
win = hg.NewWindow(480, 240)

-- create a new output surface for the newly opened window
surface = renderer:NewOutputSurface(win)
renderer:SetOutputSurface(surface)

-- initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system:Initialize(renderer)

-- create a gpu texture
pic = hg.Picture(512, 512, hg.PictureRGBA8)
tex = renderer:NewTexture("clock_tex")
if not renderer:CreateTexture(tex, pic) then
	print("Could not create clock texture")
end

-- Function to draw a clock in a picture
function draw_clock()
	-- Get the current time
	date = os.date("*t")

	-- clear the picture
	pic:ClearRGBA(31/255, 106/255, 149/255)

	-- draw a clock in the picture
	radius = pic:GetWidth() / 2

	-- draw the background circle
	pic:SetPenMode(hg.PenNone)
	pic:SetFillColorRGBA(237/255, 233/255, 230/255)
	pic:DrawCircle(pic:GetWidth() / 2, pic:GetHeight() / 2, radius)

	-- draw the hour tick
	pic:SetPenMode(hg.PenSolid)  -- draw outline of the triangle
	pic:SetPenWidth(pic:GetWidth() * 0.01)  -- thick pen width
	pic:SetPenColorRGBA(237 * 0.8/255, 233 * 0.8/255, 230 * 0.8/255)  -- select a color for the pen

	step = (2 * math.pi) / 12
	for i=0,11 do
		sub_step = i * step
		pic:MoveTo(radius + math.cos(sub_step) * radius, radius + math.sin(sub_step) * radius)  -- move the pen to the starting position
		length_step = 50
		if i % 3 == 0  then
            length_step = 70
        end
		pic:LineTo(radius + math.cos(sub_step) * (radius - length_step), radius + math.sin(sub_step) * (radius - length_step))
		pic:DrawPath()  -- draw the line
    end
	pic:SetPenMode(hg.PenNone)

	function draw_needle(angle, size, width)
		pic:MoveTo(radius - math.sin(angle) * size, radius - math.cos(angle) * size)
		pic:LineTo(radius - math.sin(angle + math.pi * 0.5) * width, radius - math.cos(angle + math.pi * 0.5) * width)
		pic:LineTo(radius - math.sin(angle + math.pi) * width, radius - math.cos(angle + math.pi) * width)
		pic:LineTo(radius - math.sin(angle - math.pi * 0.5) * width, radius - math.cos(angle - math.pi * 0.5) * width)
		pic:ClosePolygon()  -- end the path
		pic:DrawPath()  -- draw the path
    end
	-- draw hour needle
	pic:SetFillColorRGBA(0,0,0)
	draw_needle((date.hour % 12 / 12) * math.pi*2, radius * 0.6, radius * 0.075)

	-- draw minute needle
	pic:SetFillColorRGBA(0,0,0)
	draw_needle((date.min / 60) * math.pi*2, radius * 0.8, radius * 0.05)

	-- draw second needle
	pic:SetFillColorRGBA(255/255, 25/255, 0)
	draw_needle((date.sec / 60) * math.pi*2, radius * 0.9, radius * 0.015)
end

-- get keyboard device
keyboard = hg.GetInputSystem():GetDevice("keyboard")

-- continue while the window is open
while hg.IsWindowOpen(win) and (not keyboard:WasPressed(hg.KeyEscape)) do
	ok,width,height = hg.GetWindowClientSize(win)
	renderer:SetViewport(hg.Rect(0, 0, width, height))

	-- set perspective matrix
	persp_mat = hg.ComputePerspectiveProjectionMatrix(0.1, 100, 3.2, renderer:GetAspectRatio())
	renderer:SetProjectionMatrix(persp_mat)

	-- clear the viewport with green color
	renderer:Clear(hg.Color(0.05, 0.05, 0.05, 0))

	-- blit the picture with the clock in a texture
	draw_clock()
	renderer:BlitTexture(tex, pic)

	-- draw the triangle using the render system
	x, y, z, w = 2.0, 1.5, 10, 0.55
	vertices = {hg.Vector3(-x, -y + w, z*0.5), hg.Vector3(-x, y + w, z), hg.Vector3(x, y + w, z),
				hg.Vector3(-x, -y + w, z*0.5), hg.Vector3(x, y + w, z), hg.Vector3(x, -y + w, z*0.5)}
	uvs = {hg.Vector2(1, 1), hg.Vector2(1, 0), hg.Vector2(0, 0),
		   hg.Vector2(1, 1), hg.Vector2(0, 0), hg.Vector2(0, 1)}

	render_system:DrawTriangleAuto(2, vertices, {}, uvs, tex)

	renderer:DrawFrame()
	renderer:ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()
end

render_system:Free()
renderer:Close()