# Draw the mouse cursor
import gs

# mount the system file driver
gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core/")

# create the renderer
renderer = gs.EglRenderer()
renderer.Open(480, 240)

# work in 2d and in pixels
renderer.Set2DMatrices()

# initialize the render system, which is used to draw through the renderer
render_system = gs.RenderSystem()
render_system.Initialize(renderer)

# get the mouse device
mouse_device = gs.GetInputSystem().GetDevice("mouse")
mouse_pos = gs.Vector2(0, 0)

# continue while the window is open
while renderer.GetDefaultOutputWindow():

	# update input system
	gs.GetInputSystem().Update()

	# get mouse position
	mouse_pos.x = mouse_device.GetValue(gs.InputDevice.InputAxisX)
	mouse_pos.y = mouse_device.GetValue(gs.InputDevice.InputAxisY)

	# clear the viewport with green color
	renderer.Clear(gs.Color(0, 1, 0, 0))

	# draw the triangle using the render system
	vertices = [gs.Vector3(mouse_pos.x, mouse_pos.y, 0.5), gs.Vector3(mouse_pos.x + 30, mouse_pos.y, 0.5), gs.Vector3(mouse_pos.x, mouse_pos.y - 30, 0.5)]
	color = [gs.Color.Red, gs.Color.Red, gs.Color.Red]
	render_system.DrawTriangleAutoRGB(1, vertices, color)

	renderer.DrawFrame()
	renderer.ShowFrame()
	renderer.UpdateOutputWindow()
