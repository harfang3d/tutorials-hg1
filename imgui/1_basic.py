import harfang as hg

# load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

# create the renderer
renderer = hg.CreateRenderer()
renderer.Open()

# open a new window
win = hg.NewWindow(640, 480)

# create a new output surface for the newly opened window
surface = renderer.NewOutputSurface(win)
renderer.SetOutputSurface(surface)

# get keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

check = True
combo = 0
color = hg.Color(1, 0, 1)

hg.ImGuiSetOutputSurface(surface)

while hg.IsWindowOpen(win) and not keyboard.WasPressed(hg.KeyEscape):
	if hg.ImGuiBegin("GUI"):
		_,check = hg.ImGuiCheckbox("Check", check)

		if hg.ImGuiCollapsingHeader("Header", True):
			if hg.ImGuiButton("Button"):
				print("Button pressed")
		
			_,combo = hg.ImGuiCombo("Combo", combo, ['item 1', 'item 2', 'item 3'])
			_,color = hg.ImGuiColorButton("Color", color)
	
	hg.ImGuiEnd()

	renderer.Clear(hg.Color.Red)
	renderer.ShowFrame()
	hg.UpdateWindow(win)

	hg.EndFrame()

renderer.DestroyOutputSurface(surface)
hg.DestroyWindow(win)
renderer.Close()