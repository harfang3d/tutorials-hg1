import gs
import gs.plus.render as render
import gs.plus.input as input

render.init(400, 300, "../pkg.core")

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.line2d(0, 0, 400, 300, gs.Color.Red, gs.Color.Blue)
	render.flip()
