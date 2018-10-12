hg = require("harfang")

-- load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

-- create the renderer
renderer = hg.CreateRenderer()
renderer:Open()

-- open a new window
win = hg.NewWindow(640, 480)

-- create a new output surface for the newly opened window
surface = renderer:NewOutputSurface(win)
renderer:SetOutputSurface(surface)

-- get keyboard device
keyboard = hg.GetInputSystem():GetDevice("keyboard")

check = true
open = true
combo = 0
items = hg.StringList({"Item 1", "Item 2", "Item 3"})
color = hg.Color(1, 0, 1)

hg.ImGuiSetOutputSurface(surface)

while hg.IsWindowOpen(win) and not keyboard:WasPressed(hg.KeyEscape) do
	if hg.ImGuiBegin("GUI") then
		_,check = hg.ImGuiCheckbox("Check", check)
		_,open = hg.ImGuiCollapsingHeader("Header", true)
		if _ then
			if hg.ImGuiButton("Button") then
				print("Button pressed")
			end

			_,combo = hg.ImGuiCombo("Combo", combo, items)
			_,color = hg.ImGuiColorButton("Color", color)
		end
	end
	hg.ImGuiEnd()
	
	renderer:Clear(hg.Color.Red)
	renderer:ShowFrame()
	hg.UpdateWindow(win)

	hg.EndFrame()
end

renderer:DestroyOutputSurface(surface)
hg.DestroyWindow(win)
renderer:Close()