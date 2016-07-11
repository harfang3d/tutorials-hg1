# Load a picture and save it as JPEG

import os
import gs

gs.LoadPlugins(gs.get_default_plugins_path())

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture
pic = gs.LoadPicture(os.path.join(os.getcwd(), "../_data/owl.jpg"))

# IJG codec can only save RGB8
pic.Convert(gs.Picture.RGB8)

# save as JPEG in the same folder (quality set to 20%)
gs.SavePicture(pic, os.path.join(os.getcwd(), "save.jpg"), "IJG", "q:20")
