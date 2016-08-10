# Load a picture, write text to it and save the result

import os
import gs

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture
pic = gs.LoadPicture("../_data/owl.jpg")

# create a font engine and load a font
font_engine = gs.FontEngine()
font_engine.SetFont("../_data/Cabin-Regular.ttf")  # set font
font_engine.SetSize(48)  # set current font size

# render text over the picture
pic.SetFillColorRGBA(1, 1, 1)  # select a color to fill the font
pic.DrawText(font_engine, "Text Output Sample", 50, 480)

# save the result
gs.SavePicture(pic, "draw_text.png", "STB", "format:png")
