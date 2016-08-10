# Reconstruct and display the famous Cornell box, 
# which is a test scene commonly used to demonstrate radiosity.

import gs
import gs.plus.geometry
import math

box_width = 5.5
box_height = 5.6
light_width = box_width * 0.25

# mount the runtime package required for the rendering
gs.GetFilesystem().Mount(gs.StdFileDriver("../_data/"))

# create the renderer
renderer = gs.EglRenderer()
renderer.Open(720, 720)

render_system = gs.RenderSystem()
render_system.Initialize(renderer)

scene = gs.Scene()
scene.SetupCoreSystemsAndComponents(render_system)

env = gs.Environment()
env.SetBackgroundColor(gs.Color.Black)
env.SetAmbientColor(gs.Color.White)
env.SetAmbientIntensity(0.1)
scene.AddComponent(env)

# light Source Definition
node_light = gs.Node()

light_transform = gs.Transform()
light_transform.SetPosition(gs.Vector3(0.0, box_height * 0.825, 0.0))
node_light.AddComponent(light_transform)

light_component = gs.Light()
light_component.SetDiffuseColor(gs.Color(1, 0.9, 0.7))
light_component.SetRange(box_width * 10.0)
light_component.SetShadow(gs.Light.Shadow_Map)
node_light.AddComponent(light_component)

scene.AddNode(node_light)


# wall definitions
def create_wall(pos = gs.Vector3(), rot = gs.Vector3(), width = 1.0, length = 1.0, material_path = None):
	""" generic function to create a wall """
	node = gs.Node()
	transform = gs.Transform()
	transform.SetPosition(pos)
	transform.SetRotation(rot)
	node.AddComponent(transform)
	object = gs.Object()
	object.SetGeometry(render_system.CreateGeometry(gs.plus.geometry.create_plane(width = width, length = length, material_path = material_path)))
	node.AddComponent(object)
	return node


# light source geometry
scene.AddNode(create_wall(pos = gs.Vector3(0, box_height * 0.995, 0), rot = gs.Vector3(math.pi,0,0),
							width = light_width, length = light_width,
							material_path = "material_self_color.mat"))

# floor
scene.AddNode(create_wall(width = box_width, length = box_width))

# ceiling
scene.AddNode(create_wall(pos = gs.Vector3(0, box_height, 0), rot = gs.Vector3(math.pi,0,0),
							width = box_width, length = box_width))

# back_wall
scene.AddNode(create_wall(pos = gs.Vector3(0, box_height * 0.5, box_width * 0.5), rot = gs.Vector3(math.pi * -0.5, 0, 0),
							width = box_width, length = box_height))

# right_wall
scene.AddNode(create_wall(pos = gs.Vector3(box_width * 0.5, box_height * 0.5, 0), rot = gs.Vector3(0, 0, math.pi * 0.5),
							width = box_height, length = box_width,
							material_path = "material_diffuse_color_green.mat"))

# left_wall
scene.AddNode(create_wall(pos = gs.Vector3(-box_width * 0.5, box_height * 0.5, 0), rot = gs.Vector3(0, 0, math.pi * -0.5),
							width = box_height, length = box_width,
							material_path = "material_diffuse_color_red.mat"))


# box definitions
def create_box(pos = gs.Vector3(), rot = gs.Vector3(), width = 1.0, height = 1.0):
	node = gs.Node()
	object = gs.Object()
	transform = gs.Transform()
	transform.SetPosition(pos + gs.Vector3(0, height * 0.5, 0))
	transform.SetRotation(rot)
	node.AddComponent(transform)
	object.SetGeometry(render_system.CreateGeometry(gs.plus.geometry.create_cube(width, height, width)))
	node.AddComponent(object)
	return node


# short box definition
scene.AddNode(create_box(pos = gs.Vector3(box_width * 0.18, 0, box_width * -0.25),
						rot = gs.Vector3(0, math.pi * 0.085, 0),
						width = box_width * 0.3, height = box_height * 0.3))

# tall box definition
scene.AddNode(create_box(pos = gs.Vector3(box_width * -0.18, 0, box_width * 0.25),
						rot = gs.Vector3(0, math.pi * -0.085, 0),
						width = box_width * 0.35, height = box_height * 0.65))

# set up the camera position and field of view for the usual view of the box
node_camera = gs.Node()
camera_transform = gs.Transform()
camera_transform.SetPosition(gs.Vector3(0.0, box_height * 0.5, -box_width * 2.25))
node_camera.AddComponent(camera_transform)
node_camera.AddComponent(gs.Camera())
scene.AddNode(node_camera)
scene.SetCurrentCamera(node_camera)

# main rendering loop
while renderer.GetDefaultOutputWindow():
	scene.Update()
	scene.WaitUpdate()

	scene.Commit()
	scene.WaitCommit()

	renderer.ShowFrame()
	renderer.UpdateOutputWindow()
