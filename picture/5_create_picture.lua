-- Create a picture, allocate and print its dimensions

hg = require("harfang")

-- load picture, allocate and display informations
pic = hg.Picture(128, 512, hg.PictureRGBA8)

print(string.format("Picture dimensions: %dx%d", pic:GetWidth(), pic:GetHeight()))
