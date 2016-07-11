import gs
import gs.plus.render as render
import gs.plus.input as input

gs.LoadPlugins(gs.get_default_plugins_path())

render.init(512, 512, "../pkg.core")

# provide access to the data folder
gs.MountFileDriver(gs.StdFileDriver("../_data/"), "@data/")

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.image2d(0, 0, 0.25, "@data/blink.jpg")
	render.sprite2d(512 - 64, 512 - 64, 128, "@data/blink.jpg")
	render.blit2d(0, 0, 512, 512, 80, 80, 512 - 160, 512 - 160, "@data/owl.jpg")
	render.flip()
