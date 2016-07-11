import gs
import gs.plus.render as render
import gs.plus.input as input
import gs.plus.geometry as geometry

render.init(400, 300, "../pkg.core")

angle = 0
cube = render.create_geometry(geometry.create_cube())

while not input.key_press(gs.InputDevice.KeyEscape):
	render.clear()
	render.geometry2d(200, 150, cube, angle, angle * 2, 0, 100)
	render.flip()

	angle += 0.0001
