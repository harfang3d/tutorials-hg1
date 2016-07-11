import gs
import gs.plus.render as render
import gs.plus.input as input

render.init(400, 300, "../pkg.core")

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.plot2d(200, 150, gs.Color.Green)
	render.flip()
