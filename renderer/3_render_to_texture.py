# How to draw to a texture using the low-level renderer API

import os
import harfang as hg
import math

# load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

# mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

# create the renderer
renderer = hg.CreateRenderer()
renderer.Open()

# open a new window
win = hg.NewWindow(480, 240)

# create a new output surface for the newly opened window
surface = renderer.NewOutputSurface(win)
renderer.SetOutputSurface(surface)

#  load 2d shader and retrieve variables
shader_color = renderer.LoadShader("_data/shader_2d_color.isl")
shader_texture = renderer.LoadShader("_data/shader_2d_single_texture.isl")

# create primitive index buffer
data = hg.BinaryData()
data.WriteUInt16s([0,1,2])

idx = renderer.NewBuffer()
renderer.CreateBuffer(idx, data, hg.GpuBufferIndex)

# create primitive vertex buffer
vtx_layout = hg.VertexLayout()
vtx_layout.AddAttribute(hg.VertexPosition, 3, hg.VertexFloat)
vtx_layout.AddAttribute(hg.VertexUV0, 2, hg.VertexUByte, True) # UVs are sent as normalized 8 bit unsigned integer (range [0;255])

data = hg.BinaryData()

x, y = 0.5, 0.5
data.WriteFloats([-x,-y,0.5])
data.WriteUInt8s([127,0])

data.WriteFloats([-x,y,0.5])
data.WriteUInt8s([0,127])

data.WriteFloats([x,y,0.5])
data.WriteUInt8s([127,127])

vtx = renderer.NewBuffer()
renderer.CreateBuffer(vtx, data, hg.GpuBufferVertex)

# create the texture we will render to
tgt_tex = renderer.NewTexture()
renderer.CreateTexture(tgt_tex, 64, 64)

# create and configure the frame buffer object to render to the texture
tgt_rt = renderer.NewRenderTarget()
renderer.CreateRenderTarget(tgt_rt)
renderer.SetRenderTargetColorTexture(tgt_rt, tgt_tex)

# get keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

# draw loop
print("Close the renderer window or press Ctrl+C in this window to end")

while hg.IsWindowOpen(win) and (not keyboard.WasPressed(hg.KeyEscape)):
	# first render a blue triangle on a green background to the texture using the
	# render target
	renderer.SetRenderTarget(tgt_rt)

	renderer.SetViewport(hg.Rect(0, 0, 64, 64)) # fit viewport to texture dimensions
	renderer.Clear(hg.Color.Green)

	renderer.SetShader(shader_color)
	renderer.SetShaderFloat4("u_color", 0, 0, 1, 1) # blue
	hg.DrawBuffers(renderer, 3, idx, vtx, vtx_layout)

	# switch back to the default render target and display the texture we just
	# rendered to using a triangle on a red background

	# note that the UVs are skewed so that the triangle drawn into the texture
	# does not exactly overlap with the triangle used to display the texture
	renderer.ClearRenderTarget()

	_,wx,wy = hg.GetWindowClientSize(win)
	renderer.SetViewport(hg.Rect(0, 0, wx, wy)) # fit viewport to window dimensions
	renderer.Clear(hg.Color.Red)

	renderer.SetShader(shader_texture)
	renderer.SetShaderTexture("u_tex", tgt_tex)
	hg.DrawBuffers(renderer, 3, idx, vtx, vtx_layout)

	renderer.DrawFrame()
	renderer.ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()

renderer.DestroyOutputSurface(surface)
hg.DestroyWindow(win)
renderer.Close()