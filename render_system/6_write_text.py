# How to draw text using TTF fonts with the render system

import gs

# mount the system file driver
gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core")

# create the renderer and render system
egl = gs.EglRenderer()
egl.Open(860, 56)

sys = gs.RenderSystem()
sys.Initialize(egl)

# create the font object
font = gs.RasterFont("@core/fonts/default.ttf", 48, 512)

# set default render states
egl.Set2DMatrices()
egl.EnableBlending(True)
egl.EnableDepthTest(False)

while egl.GetDefaultOutputWindow():
	egl.Clear(gs.Color.Black)

	# draw baseline
	sys.DrawLineAutoRGB(1, [gs.Vector3(0, 10, 0.5), gs.Vector3(1000, 10, 0.5)], [gs.Color.Red, gs.Color.Red])
	# draw text
	font.Write(sys, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", gs.Vector3(0, 10, 0.5))

	sys.DrawRasterFontBatch()

	egl.ShowFrame()
	egl.UpdateOutputWindow()

font = None
