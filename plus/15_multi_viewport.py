import gs
import gs.plus.clock as clock
import gs.plus.input as input
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.geometry as geometry

render.init(640, 400, "../pkg.core")

cube = render.create_geometry(geometry.create_cube(0.5, 2, 0.5))

fps = camera.fps_controller(0, 2, -10)
fps.rot.x = 0.5

size = render.get_renderer().GetCurrentOutputWindow().GetSize()

def draw_view(viewport, cam_pos, cam_rot):
	render.get_renderer().SetViewport(viewport)
	render.get_renderer().SetClippingRect(viewport)

	render.get_renderer().Clear(gs.Color.Black)

	render.set_camera3d(cam_pos.x, cam_pos.y, cam_pos.z, cam_rot.x, cam_rot.y, cam_rot.z)

	for z in range(-50, 50, 5):
		for x in range(-50, 50, 5):
			render.geometry3d(x, 0, z, cube)


while not input.key_press(gs.InputDevice.KeyEscape):

	fps.update(clock.update())

	# draw the full view at fps position
	draw_view(gs.fRect(0, 0, size.x, size.y), fps.pos, fps.rot)

	# process the view on screen
	render.get_renderer().DrawFrame()
	render.commit_2d()
	render.commit_3d()

	# draw the vignette on left bottom side with another point of view
	draw_view(gs.fRect(0, 0, size.x*0.5, size.y*0.5), fps.pos + gs.Vector3(0, 15, 0), fps.rot)

	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around")

	# send the final rendered image on screen
	render.flip()
