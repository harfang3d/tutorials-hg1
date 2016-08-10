# Display a scene using isometric projection

import gs
import math

# create the renderer
plus = gs.GetPlus()
plus.RenderInit(1280, 720)

# configure scene
scn = plus.NewScene()
plus.AddEnvironment(scn, gs.Color(0, 0, 0.1), gs.Color(0.1, 0.1, 0.2))

cam = plus.AddCamera(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(0, 0.5, -2), gs.Vector3(0.25, 0, 0)), True)
cam.GetCamera().SetOrthographicSize(1.3)
cam.GetCamera().SetZNear(0.1)
cam.GetCamera().SetZFar(10)

plus.AddLight(scn, gs.Matrix4.TransformationMatrix(gs.Vector3.Zero, gs.Vector3(0.075, 0, 0)), gs.Light.Model_Linear, 50)
plus.AddPlane(scn, gs.Matrix4.Identity, 1, 1)

# create a few boxes
boxes = []
for i in range(63):
	box = plus.AddCube(scn, gs.Matrix4.Identity, 0.1, 0.25, 0.1)
	boxes.append(box)

# main rendering loop
t = 0
while not plus.KeyPress(gs.InputDevice.KeyEscape):
	# get the boxes dancing
	t += plus.UpdateClock().to_sec()

	for i, box in enumerate(boxes):
		t_ = t + i * 0.1
		pos = gs.Vector3(math.cos(t_), 0, math.sin(t_))
		rot = gs.Vector3(t_ * 2, t_ * -3, t_ + t * 4)
		box.GetTransform().SetWorld(gs.Matrix4.TransformationMatrix(pos, rot, gs.Vector3.One))

	plus.UpdateScene(scn, gs.time(0))
	plus.Flip()
