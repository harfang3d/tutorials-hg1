# Load a picture and print its dimensions

import os
import gs

gs.LoadPlugins(gs.get_default_plugins_path())

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture and display informations
pic = gs.LoadPicture(os.path.join(os.getcwd(), "../_data/owl.jpg"))

print("Picture dimensions: %dx%d" % (pic.GetWidth(), pic.GetHeight()))
