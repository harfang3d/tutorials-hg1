import gs
import gs.plus.render as render
import gs.plus.input as input

render.init(400, 300, "../pkg.core")

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.triangle2d(40, 40, 200, 260, 360, 40, gs.Color.Red, gs.Color.Blue, gs.Color.Green)
	render.flip()
