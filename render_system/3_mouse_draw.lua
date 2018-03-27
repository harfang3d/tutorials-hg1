-- Draw the mouse cursor

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

-- work in 2d and in pixels
renderer:Set2DMatrices()

-- initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system:Initialize(renderer)

-- get keyboard device
keyboard = hg.GetInputSystem():GetDevice("keyboard")

-- get the mouse device
mouse_device = hg.GetInputSystem():GetDevice("mouse")
mouse_pos = hg.Vector2(0, 0)

-- continue while the window is open
while hg.IsWindowOpen(win) and (not keyboard:WasPressed(hg.KeyEscape)) do
	-- update input system
	hg.GetInputSystem():Update()

	-- get mouse position
	mouse_pos.x = mouse_device:GetValue(hg.InputAxisX)
	mouse_pos.y = mouse_device:GetValue(hg.InputAxisY)

	-- clear the viewport with green color
	renderer:Clear(hg.Color(0, 1, 0, 0))

	-- draw the triangle using the render system
	vertices = {hg.Vector3(mouse_pos.x, mouse_pos.y, 0.5), hg.Vector3(mouse_pos.x + 30, mouse_pos.y, 0.5), hg.Vector3(mouse_pos.x, mouse_pos.y - 30, 0.5)}
	color = {hg.Color.Red, hg.Color.Red, hg.Color.Red}
	render_system:DrawTriangleAuto(1, vertices, color)

	renderer:DrawFrame()
	renderer:ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()
end