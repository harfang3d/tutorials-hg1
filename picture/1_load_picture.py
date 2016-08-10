# Load a picture and print its dimensions

import os
import gs

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture and display informations
pic = gs.LoadPicture("../_data/owl.jpg")

print("Picture dimensions: %dx%d" % (pic.GetWidth(), pic.GetHeight()))
