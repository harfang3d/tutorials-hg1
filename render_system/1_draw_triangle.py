# How to draw a primitive using the mid-level render system API

import os
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

# work in 2d and in pixels
renderer.Set2DMatrices()

# initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system.Initialize(renderer)

# get keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

# continue while the window is open
while hg.IsWindowOpen(win) and (not keyboard.WasPressed(hg.KeyEscape)):
	# clear the viewport with green color
	renderer.Clear(hg.Color.Green)

	# draw the triangle using the render system
	vertices = [hg.Vector3(0, 0, 0), hg.Vector3(0, 240, 0), hg.Vector3(480, 240, 0)]
	color = [hg.Color.Red, hg.Color.Green, hg.Color.Blue]
	render_system.DrawTriangleAuto(1, vertices, color)

	renderer.DrawFrame()
	renderer.ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()
