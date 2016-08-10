# Load a picture and save it as JPEG

import os
import gs

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load picture
pic = gs.LoadPicture("../_data/owl.jpg")

# IJG codec can only save RGB8
pic.Convert(gs.Picture.RGB8)

# save as JPEG in the same folder (quality set to 20%)
gs.SavePicture(pic, "save.jpg", "IJG", "q:20")
