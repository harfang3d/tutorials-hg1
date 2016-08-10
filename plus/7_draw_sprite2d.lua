gs.LoadPlugins()

plus = gs.GetPlus()
plus:RenderInit(512, 512)

-- provide access to the data folder
gs.MountFileDriver(gs.StdFileDriver('../_data/'), '@data/')

while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	plus:Clear()
	plus:Image2D(0, 0, 0.25, '@data/blink.jpg')
	plus:Sprite2D(512 - 64, 512 - 64, 128, '@data/blink.jpg')
	plus:Blit2D(0, 0, 512, 512, 80, 80, 512 - 160, 512 - 160, '@data/owl.jpg')
	plus:Flip()
end
