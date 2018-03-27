# How to draw text using TTF fonts with the render system

import harfang as hg

# load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

# create the renderer
renderer = hg.CreateRenderer()
renderer.Open()

# open a new window
win = hg.NewWindow(860, 200)

# create a new output surface for the newly opened window
surface = renderer.NewOutputSurface(win)
renderer.SetOutputSurface(surface)

# initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system.Initialize(renderer)

# create the font object
font = hg.RasterFont("@core/fonts/default.ttf", 48, 512)

# set default render states
renderer.Set2DMatrices()
renderer.EnableBlending(True)
renderer.EnableDepthTest(False)

# get keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

while hg.IsWindowOpen(win) and (not keyboard.WasPressed(hg.KeyEscape)):
	renderer.Clear(hg.Color.Black)

	# draw baseline
	render_system.DrawLineAuto(1, [hg.Vector3(0, 10, 0.5), hg.Vector3(1000, 10, 0.5)], [hg.Color.Red, hg.Color.Red])
	# draw text
	font.Write(render_system, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", hg.Matrix4.TranslationMatrix(hg.Vector3(0, 10, 0.5)))

	render_system.DrawRasterFontBatch()

	renderer.DrawFrame()
	renderer.ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()

font = None
