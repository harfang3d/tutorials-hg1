-- Load a picture, write text to it and save the result

hg = require("harfang")

hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- load picture
pic = hg.Picture()
hg.LoadPicture(pic, "_data/owl.jpg")

-- create a font engine and load a font
font_engine = hg.FontEngine()
font_engine:SetFont("_data/Cabin-Regular.ttf")  -- set font
font_engine:SetSize(48)  -- set current font size

-- render text over the picture
pic:SetFillColorRGBA(1, 1, 1)  -- select a color to fill the font
pic:DrawText(font_engine, "Text Output Sample", 50, 480)

-- save the result
hg.SavePicture(pic, "draw_text.png", "STB", "format:png")
