-- Load a picture and save it as JPEG

hg = require("harfang")

hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- load picture
pic = hg.Picture()
ok = hg.LoadPicture(pic, "_data/owl.jpg")

-- IJG codec can only save RGB8
pic:Convert(hg.PictureRGB8)

-- save as JPEG in the same folder (quality set to 20%)
hg.SavePicture(pic, "save.jpg", "IJG", "q:20")
