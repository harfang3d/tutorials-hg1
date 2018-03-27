-- Load a picture and print its dimensions

hg = require("harfang")

hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- load picture and display informations
pic = hg.Picture()
ok = hg.LoadPicture(pic, "_data/owl.jpg")
if not ok then
	print("Failed to load image!")
else
	print(string.format("Picture dimensions: %dx%d", pic:GetWidth(), pic:GetHeight()))
end
