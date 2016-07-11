# How to draw a picture on a primitive

import os
import gs
import math

# mount the system file driver
gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core/")

# create the renderer
renderer = gs.EglRenderer()
renderer.Open(480, 480)

# initialize the render system, which is used to draw through the renderer
render_system = gs.RenderSystem()
render_system.Initialize(renderer)

# create a gpu texture
pic = gs.Picture(512, 512, gs.Picture.RGBA8)
tex = renderer.NewTexture("clock_tex")
if not renderer.CreateTexture(tex, pic):
	print("Could not create clock texture")


def draw_clock():
	""" Function to draw a clock in a picture """
	# Get the current time
	import datetime
	date = datetime.datetime.now()

	# clear the picture
	pic.ClearRGBA(31/255, 106/255, 149/255)

	# draw a clock in the picture
	radius = pic.GetWidth() / 2

	# draw the background circle
	pic.SetPenMode(gs.Picture.PenNone)
	pic.SetFillColorRGBA(237/255, 233/255, 230/255)
	pic.DrawCircle(pic.GetWidth() / 2, pic.GetHeight() / 2, radius)

	# draw the hour tick
	pic.SetPenMode(gs.Picture.PenSolid)  # draw outline of the triangle
	pic.SetPenWidth(pic.GetWidth() * 0.01)  # thick pen width
	pic.SetPenColorRGBA(237 * 0.8/255, 233 * 0.8/255, 230 * 0.8/255)  # select a color for the pen

	step = (2 * math.pi) / 12
	for i in range(12):
		sub_step = i * step
		pic.MoveTo(radius + math.cos(sub_step) * radius, radius + math.sin(sub_step) * radius)  # move the pen to the starting position
		length_step = 50
		if i % 3 == 0:
			length_step = 70
		pic.LineTo(radius + math.cos(sub_step) * (radius - length_step), radius + math.sin(sub_step) * (radius - length_step))
		pic.DrawPath()  # draw the line

	pic.SetPenMode(gs.Picture.PenNone)

	def draw_needle(angle, size, width):
		pic.MoveTo(radius - math.sin(angle) * size, radius - math.cos(angle) * size)
		pic.LineTo(radius - math.sin(angle + math.pi * 0.5) * width, radius - math.cos(angle + math.pi * 0.5) * width)
		pic.LineTo(radius - math.sin(angle + math.pi) * width, radius - math.cos(angle + math.pi) * width)
		pic.LineTo(radius - math.sin(angle - math.pi * 0.5) * width, radius - math.cos(angle - math.pi * 0.5) * width)
		pic.ClosePolygon()  # end the path
		pic.DrawPath()  # draw the path

	# draw hour needle
	pic.SetFillColorRGBA(0,0,0)
	draw_needle((date.hour % 12 / 12) * math.pi*2, radius * 0.6, radius * 0.075)

	# draw minute needle
	pic.SetFillColorRGBA(0,0,0)
	draw_needle((date.minute / 60) * math.pi*2, radius * 0.8, radius * 0.05)

	# draw second needle
	pic.SetFillColorRGBA(255/255, 25/255, 0)
	draw_needle((date.second / 60) * math.pi*2, radius * 0.9, radius * 0.015)


# continue while the window is open
while renderer.GetDefaultOutputWindow():
	size = renderer.GetDefaultOutputWindow().GetSize()
	renderer.SetViewport(gs.fRect(0, 0, size.x, size.y))

	# set perspective matrix
	persp_mat = gs.ComputePerspectiveProjectionMatrix(0.1, 100, 3.2, renderer.GetAspectRatio())
	renderer.SetProjectionMatrix(persp_mat)

	# clear the viewport with green color
	renderer.Clear(gs.Color(0.05, 0.05, 0.05, 0))

	# blit the picture with the clock in a texture
	draw_clock()
	renderer.BlitTexture(tex, pic)

	# draw the triangle using the render system
	x, y, z, w = 2.0, 1.5, 10, 0.55
	vertices = [gs.Vector3(-x, -y + w, z*0.5), gs.Vector3(-x, y + w, z), gs.Vector3(x, y + w, z),
				gs.Vector3(-x, -y + w, z*0.5), gs.Vector3(x, y + w, z), gs.Vector3(x, -y + w, z*0.5)]
	uvs = [gs.Vector2(1, 1), gs.Vector2(1, 0), gs.Vector2(0, 0),
		   gs.Vector2(1, 1), gs.Vector2(0, 0), gs.Vector2(0, 1)]

	render_system.DrawTriangleAutoUV(2, vertices, uvs, tex)

	renderer.DrawFrame()
	renderer.ShowFrame()
	renderer.UpdateOutputWindow()
