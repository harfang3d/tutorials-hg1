import gs
import gs.plus.render as render
import gs.plus.input as input

render.init(400, 300, "../pkg.core")

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.text2d(120, 150, "Draw Text Example")
	render.flip()
