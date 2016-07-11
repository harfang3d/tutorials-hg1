import gs
import gs.plus.render as render
import gs.plus.input as input

render.init(400, 300, "../pkg.core")

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.text2d(20, 200, "UNDER", 64)
	render.triangle2d(0 + 75, 150 - 50, 100 + 75, 300 - 50, 200 + 75, 150 - 50, gs.Color.Red, gs.Color.Blue, gs.Color.Green)
	render.line2d(0, 0, 400, 300)
	render.triangle2d(200 - 75, 0 + 50, 300 - 75, 150 + 50, 400 - 75, 0 + 50, gs.Color.Red, gs.Color.Blue, gs.Color.Green)
	render.text2d(200, 50, "OVER", 64)
	render.set_blend_mode2d(render.BlendAdditive)
	render.text2d(120, 135, "ADDITIVE", 32, gs.Color.Blue)
	render.set_blend_mode2d(render.BlendOpaque)
	render.flip()
