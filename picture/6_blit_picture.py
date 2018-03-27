# Blit from a picture to another picture

import os
import harfang as hg

hg.LoadPlugins()

# mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

# load pictures
owl = hg.Picture()
hg.LoadPicture(owl, "_data/owl.jpg")
blink = hg.Picture()
hg.LoadPicture(blink, "_data/blink.jpg")

# blit the center portion of the blinking owl to the lower right corner of the owl picture
owl.Blit(blink, hg.IntRect(128, 128, 384, 384), hg.IntVector2(256, 256))

# blit and stretch the complete blinking owl to the lower left corner of the owl picture
owl.Blit(blink, hg.IntRect(0, 0, 512, 512), hg.IntRect(0, 256, 256, 512), hg.FilterBlackman36)

owl.Convert(hg.PictureRGB8)
hg.SavePicture(owl, "blit_picture.jpg", "IJG", "q:100")
