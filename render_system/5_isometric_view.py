# Display a scene using isometric projection

import harfang as hg
import math

hg.LoadPlugins()

# create the renderer
plus = hg.GetPlus()
plus.RenderInit(1280, 720)

# configure scene
scn = plus.NewScene()
plus.AddEnvironment(scn, hg.Color(0, 0, 0.1), hg.Color(0.1, 0.1, 0.2))

cam = plus.AddCamera(scn, hg.Matrix4.TransformationMatrix(hg.Vector3(0, 0.5, -2), hg.Vector3(0.25, 0, 0)), True)
cam.GetCamera().SetOrthographicSize(1.3)
cam.GetCamera().SetZNear(0.1)
cam.GetCamera().SetZFar(10)

plus.AddLight(scn, hg.Matrix4.TransformationMatrix(hg.Vector3.Zero, hg.Vector3(0.075, 0, 0)), hg.LightModelLinear, 50)
plus.AddPlane(scn, hg.Matrix4.Identity, 1, 1)

# create a few boxes
boxes = []
for i in range(63):
	box = plus.AddCube(scn, hg.Matrix4.Identity, 0.1, 0.25, 0.1)
	boxes.append(box)

# main rendering loop
t = 0
while not plus.IsAppEnded():
	# get the boxes dancing
	t += hg.time_to_sec_f(plus.UpdateClock())

	for i, box in enumerate(boxes):
		t_ = t + i * 0.1
		pos = hg.Vector3(math.cos(t_), 0, math.sin(t_))
		rot = hg.Vector3(t_ * 2, t_ * -3, t_ + t * 4)
		box.GetTransform().SetWorld(hg.Matrix4.TransformationMatrix(pos, rot, hg.Vector3.One))

	# Update the scenegraph, process the render
	plus.UpdateScene(scn)
	plus.Flip()
	plus.EndFrame()

# Release all render ressources and close the screen
plus.RenderUninit()
