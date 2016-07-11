# Load a picture, write text to it and save the result

import os
import gs

gs.LoadPlugins(gs.get_default_plugins_path())

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture
pic = gs.LoadPicture(os.path.join(os.getcwd(), "../_data/owl.jpg"))

# create a font engine and load a font
font_engine = gs.FontEngine()
font_engine.SetFont(os.path.join(os.getcwd(), "../_data/Cabin-Regular.ttf"))  # set font
font_engine.SetSize(48)  # set current font size

# render text over the picture
pic.SetFillColorRGBA(1, 1, 1)  # select a color to fill the font
pic.DrawText(font_engine, "Text Output Sample", 50, 480)

# save the result
gs.SavePicture(pic, os.path.join(os.getcwd(), "draw_text.png"), "STB", "format:png")
