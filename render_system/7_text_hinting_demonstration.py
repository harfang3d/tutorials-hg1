# Demonstrate the effect of hinting and grid snapping on text rendering with raster font

import harfang as hg

hg.LoadPlugins()

# create the renderer
renderer = hg.CreateRenderer()
renderer.Open()

# open a new window
win = hg.NewWindow(1000, 1000)

# create a new output surface for the newly opened window
surface = renderer.NewOutputSurface(win)
renderer.SetOutputSurface(surface)

# initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system.Initialize(renderer)

# create the font objects
no_hint_fonts = []
for size in range(4, 44):
	no_hint_fonts.append(hg.RasterFont("@core/fonts/default.ttf", size, 512))

hint_fonts = []
for size in range(4, 44):
	hint_fonts.append(hg.RasterFont("@core/fonts/default.ttf", size, 512, 2, True))

# set default render states
renderer.Set2DMatrices()
renderer.EnableBlending(True)
renderer.EnableDepthTest(False)

hinting = False
glyph_snap = True

# retrieve the keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

while hg.IsWindowOpen(win) and (not keyboard.WasPressed(hg.KeyEscape)):
	renderer.Clear(hg.Color.Black)

	# catch key press
	if keyboard.WasPressed(hg.KeyNumpad1):
		hinting = not hinting
	if keyboard.WasPressed(hg.KeyNumpad2):
		glyph_snap = not glyph_snap

	# display instructions
	no_hint_fonts[12].Write(render_system, "Press 1 to toggle hinting, 2 to toggle glyph snap", hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1000 - 16, 0.5)))
	no_hint_fonts[12].Write(render_system, "Hinting: %s" % str(hinting), hg.Matrix4.TranslationMatrix(hg.Vector3(40, 1000 - 36, 0.5)), hg.Color.Green if hinting else hg.Color.Red)
	no_hint_fonts[12].Write(render_system, "Glyph snap: %s" % str(glyph_snap), hg.Matrix4.TranslationMatrix(hg.Vector3(230, 1000 - 36, 0.5)), hg.Color.Green if glyph_snap else hg.Color.Red)

	# display the list of fonts
	cursor = hg.Vector3(0, 10, 0.5)
	for font in (hint_fonts if hinting else no_hint_fonts):
		rect = font.GetTextRect(render_system, "ABCDEFGHIJKLMNOPQRSTUVWXYZ - VA")
		font.Write(render_system, "ABCDEFGHIJKLMNOPQRSTUVWXYZ - VA", hg.Matrix4.TranslationMatrix(cursor), hg.Color.White, 1, glyph_snap, True)
		cursor.y += rect.GetHeight()
	render_system.DrawRasterFontBatch()

	renderer.DrawFrame()
	renderer.ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()
	
font = None

render_system.Free()
renderer.Close()