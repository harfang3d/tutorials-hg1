# Create a picture, allocate and print its dimensions

import gs

# load picture, allocate and display informations
pic = gs.Picture(128, 512, gs.Picture.RGBA8)

print("Picture dimensions: %dx%d" % (pic.GetWidth(), pic.GetHeight()))
