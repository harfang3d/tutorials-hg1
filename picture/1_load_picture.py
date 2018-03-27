# Load a picture and print its dimensions

import os
import harfang as hg

hg.LoadPlugins()

# mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

# load picture and display informations
pic = hg.Picture()
ok = hg.LoadPicture(pic, "_data/owl.jpg")
if not ok:
	print("Failed to load image!")
else:
	print("Picture dimensions: %dx%d" % (pic.GetWidth(), pic.GetHeight()))
