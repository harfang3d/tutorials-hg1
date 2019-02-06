# Reconstruct and display the famous Cornell box, 
# which is a test scene commonly used to demonstrate radiosity.

import harfang as hg
import math

box_width = 5.5
box_height = 5.6
light_width = box_width * 0.25

# load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

# mount the runtime package required for the rendering
hg.MountFileDriver(hg.StdFileDriver("_data"))

# create the renderer
renderer = hg.CreateRenderer()
renderer.Open()

# open a new window
win = hg.NewWindow(800, 600)

# create a new output surface for the newly opened window
surface = renderer.NewOutputSurface(win)
renderer.SetOutputSurface(surface)

# initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system.Initialize(renderer)

# create scene
scene = hg.Scene()
hg.SceneSetupCoreSystemsAndComponents(scene, render_system)

env = hg.Environment()
env.SetBackgroundColor(hg.Color.Black)
env.SetAmbientColor(hg.Color.White)
env.SetAmbientIntensity(0.1)
scene.AddComponent(env)

# light Source Definition
node_light = hg.Node()

light_transform = hg.Transform()
light_transform.SetPosition(hg.Vector3(0.0, box_height * 0.825, 0.0))
node_light.AddComponent(light_transform)

light_component = hg.Light()
light_component.SetDiffuseColor(hg.Color(1, 0.9, 0.7))
light_component.SetRange(box_width * 10.0)
light_component.SetShadow(hg.LightShadowMap)
node_light.AddComponent(light_component)

scene.AddNode(node_light)

# wall definitions
def create_wall(pos = hg.Vector3.Zero, rot = hg.Vector3.Zero, width = 1.0, length = 1.0, material_path = "material_diffuse_color.mat", name="dummy"):
	""" generic function to create a wall """
	node = hg.Node()
	transform = hg.Transform()
	transform.SetPosition(pos)
	transform.SetRotation(rot)
	node.AddComponent(transform)
	object = hg.Object()
	object.SetGeometry(render_system.CreateGeometry(hg.CreatePlane(width, length, 1, material_path, name)))
	node.AddComponent(object)
	return node


# light source geometry
scene.AddNode(create_wall(pos = hg.Vector3(0, box_height * 0.995, 0), rot = hg.Vector3(math.pi,0,0),
							width = light_width, length = light_width,
							material_path = "material_self_color.mat", name="light"))

# floor
scene.AddNode(create_wall(width = box_width, length = box_width, name="floor"))

# ceiling
scene.AddNode(create_wall(pos = hg.Vector3(0, box_height, 0), rot = hg.Vector3(math.pi,0,0),
							width = box_width, length = box_width, name="ceiling"))

# back_wall
scene.AddNode(create_wall(pos = hg.Vector3(0, box_height * 0.5, box_width * 0.5), rot = hg.Vector3(math.pi * -0.5, 0, 0),
							width = box_width, length = box_height, name="back"))

# right_wall
scene.AddNode(create_wall(pos = hg.Vector3(box_width * 0.5, box_height * 0.5, 0), rot = hg.Vector3(0, 0, math.pi * 0.5),
							width = box_height, length = box_width,
							material_path = "material_diffuse_color_green.mat", name="right"))

# left_wall
scene.AddNode(create_wall(pos = hg.Vector3(-box_width * 0.5, box_height * 0.5, 0), rot = hg.Vector3(0, 0, math.pi * -0.5),
							width = box_height, length = box_width,
							material_path = "material_diffuse_color_red.mat", name="left"))


# box definitions
def create_box(pos = hg.Vector3(), rot = hg.Vector3(), width = 1.0, height = 1.0):
	node = hg.Node()
	object = hg.Object()
	transform = hg.Transform()
	transform.SetPosition(pos + hg.Vector3(0, height * 0.5, 0))
	transform.SetRotation(rot)
	node.AddComponent(transform)
	object.SetGeometry(render_system.CreateGeometry(hg.CreateCube(width, height, width)))
	node.AddComponent(object)
	return node


# short box definition
scene.AddNode(create_box(pos = hg.Vector3(box_width * 0.18, 0, box_width * -0.25),
						rot = hg.Vector3(0, math.pi * 0.085, 0),
						width = box_width * 0.3, height = box_height * 0.3))

# tall box definition
scene.AddNode(create_box(pos = hg.Vector3(box_width * -0.18, 0, box_width * 0.25),
						rot = hg.Vector3(0, math.pi * -0.085, 0),
						width = box_width * 0.35, height = box_height * 0.65))

# set up the camera position and field of view for the usual view of the box
node_camera = hg.Node()
camera_transform = hg.Transform()
camera_transform.SetPosition(hg.Vector3(0.0, box_height * 0.5, -box_width * 2.25))
node_camera.AddComponent(camera_transform)
node_camera.AddComponent(hg.Camera())
scene.AddNode(node_camera)
scene.SetCurrentCamera(node_camera)

# get keyboard device
keyboard = hg.GetInputSystem().GetDevice("keyboard")

# main rendering loop
while hg.IsWindowOpen(win) and (not keyboard.WasPressed(hg.KeyEscape)):
	scene.Update()
	scene.WaitUpdate()

	scene.Commit()
	scene.WaitCommit()

	renderer.ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()

render_system.Free()
renderer.Close()