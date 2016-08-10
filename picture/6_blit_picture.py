# Blit from a picture to another picture

import os
import gs

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# load pictures
owl = gs.LoadPicture("../_data/owl.jpg")
blink = gs.LoadPicture("../_data/blink.jpg")

# blit the center portion of the blinking owl to the lower right corner of the owl picture
owl.Blit(blink, gs.iRect(128, 128, 384, 384), gs.iVector2(256, 256))

# blit and stretch the complete blinking owl to the lower left corner of the owl picture
owl.Blit(blink, gs.iRect(0, 0, 512, 512), gs.iRect(0, 256, 256, 512), gs.Picture.Blackman256)

gs.SavePicture(owl, "blit_picture.jpg", "IJG", "q:100")
