# Create a picture, allocate and print its dimensions

import harfang as hg

# load picture, allocate and display informations
pic = hg.Picture(128, 512, hg.PictureRGBA8)

print("Picture dimensions: %dx%d" % (pic.GetWidth(), pic.GetHeight()))
