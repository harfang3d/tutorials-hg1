# Load a picture, draw to it and save the result

import os
import gs

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture
pic = gs.LoadPicture("../_data/owl.jpg")

# draw a triangle over the picture
pic.SetPenMode(gs.Picture.PenSolid)  # draw outline of the triangle
pic.SetPenWidth(10)  # thick pen width
pic.SetPenColorRGBA(0.8, 0.5, 0.7)  # select a color for the pen
pic.SetFillMode(gs.Picture.BrushNone)  # skip filling the triangle

pic.MoveTo(256, 0 + 10)  # move the pen to the starting position
pic.LineTo(512 - 10, 512 - 10)  # connect to the bottom-right corner
pic.LineTo(0 + 10, 512 - 10)  # connect to the bottom-left corner
pic.ClosePolygon()  # end the path
pic.DrawPath()  # draw the path

# save the result
gs.SavePicture(pic, "draw_vector.png", "STB", "format:png")
