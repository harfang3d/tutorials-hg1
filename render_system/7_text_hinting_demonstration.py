# Demonstrate the effect of hinting and grid snapping on text rendering with raster font

import gs

# mount the system file driver
gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core")

# create the renderer and render system
egl = gs.EglRenderer()
egl.Open(1000, 1000)

sys = gs.RenderSystem()
sys.Initialize(egl)

# create the font objects
no_hint_fonts = []
for size in range(4, 44):
	no_hint_fonts.append(gs.RasterFont("@core/fonts/default.ttf", size, 512))

hint_fonts = []
for size in range(4, 44):
	hint_fonts.append(gs.RasterFont("@core/fonts/default.ttf", size, 512, 2, True))

# set default render states
egl.Set2DMatrices()
egl.EnableBlending(True)
egl.EnableDepthTest(False)

hinting = False
glyph_snap = True

# retrieve the keyboard device
keyboard = gs.GetInputSystem().GetDevice("keyboard")

while egl.GetDefaultOutputWindow():
	egl.Clear(gs.Color.Black)

	# catch key press
	gs.GetInputSystem().Update()

	if keyboard.WasPressed(gs.InputDevice.KeyNumpad1):
		hinting = not hinting
	if keyboard.WasPressed(gs.InputDevice.KeyNumpad2):
		glyph_snap = not glyph_snap

	# display instructions
	no_hint_fonts[12].Write(sys, "Press 1 to toggle hinting, 2 to toggle glyph snap", gs.Vector3(0, 1000 - 16, 0.5))
	no_hint_fonts[12].Write(sys, "Hinting: %s" % str(hinting), gs.Vector3(40, 1000 - 36, 0.5), gs.Color.Green if hinting else gs.Color.Red)
	no_hint_fonts[12].Write(sys, "Glyph snap: %s" % str(glyph_snap), gs.Vector3(230, 1000 - 36, 0.5), gs.Color.Green if glyph_snap else gs.Color.Red)

	# display the list of fonts
	cursor = gs.Vector3(0, 10, 0.5)
	for font in (hint_fonts if hinting else no_hint_fonts):
		rect = font.GetTextRect(sys, "ABCDEFGHIJKLMNOPQRSTUVWXYZ - VA")
		font.Write(sys, "ABCDEFGHIJKLMNOPQRSTUVWXYZ - VA", cursor, gs.Color.White, 1, glyph_snap)
		cursor.y += rect.GetHeight()
	sys.DrawRasterFontBatch()

	egl.ShowFrame()
	egl.UpdateOutputWindow()

font = None
