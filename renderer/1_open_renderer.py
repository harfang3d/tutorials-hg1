import harfang as hg

# load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

# create the renderer
renderer = hg.CreateRenderer()
renderer.Open()

# open a new window
win = hg.NewWindow(480, 240)

# create a new output surface for the newly opened window
surface = renderer.NewOutputSurface(win)
renderer.SetOutputSurface(surface)

# get keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

# draw loop
print("Close the renderer window or press Ctrl+C in this window to end")

while hg.IsWindowOpen(win) and (not keyboard.WasPressed(hg.KeyEscape)):
	renderer.Clear(hg.Color.Red)

	renderer.DrawFrame()
	renderer.ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()

renderer.DestroyOutputSurface(surface)
hg.DestroyWindow(win)
renderer.Close()