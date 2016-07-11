# How to draw a primitive using the mid-level render system API

import os
import gs

# mount the system file driver
gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core/")

# create the renderer
renderer = gs.EglRenderer()
renderer.Open(480, 240)

# work in 2d and in pixels
renderer.Set2DMatrices()

# initialize the render system, which is used to draw through the renderer
render_system = gs.RenderSystem()
render_system.Initialize(renderer)

# continue while the window is open
while renderer.GetDefaultOutputWindow():
	# clear the viewport with green color
	renderer.Clear(gs.Color.Green)

	# draw the triangle using the render system
	vertices = [gs.Vector3(0, 0, 0), gs.Vector3(0, 240, 0), gs.Vector3(480, 240, 0)]
	color = [gs.Color.Red, gs.Color.Green, gs.Color.Blue]
	render_system.DrawTriangleAutoRGB(1, vertices, color)

	renderer.DrawFrame()
	renderer.ShowFrame()
	renderer.UpdateOutputWindow()
