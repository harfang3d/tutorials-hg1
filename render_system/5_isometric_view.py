# Display a scene using isometric projection

import gs
import math
import gs.plus.scene as scene
import gs.plus.render as render
import gs.plus.input as input


# mount core resources
gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core")

# create the renderer
render.init(1280, 720, "../pkg.core")

# configure scene
scn = scene.new_scene()
scene.add_environment(scn, gs.Color(0, 0, 0.1), gs.Color(0.1, 0.1, 0.2))

cam = scene.add_camera(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(0, 0.5, -2), gs.Vector3(0.25, 0, 0)), orthographic=True)
cam.GetCamera().SetOrthographicSize(1.3)
cam.GetCamera().SetZNear(0.1)
cam.GetCamera().SetZFar(10)

scene.add_light(scn, gs.Matrix4.TransformationMatrix(gs.Vector3.Zero, gs.Vector3(0.075, 0, 0)), gs.Light.Model_Linear, 50)
scene.add_plane(scn, width=1, depth=1)

# create a few boxes
boxes = []
for i in range(63):
	box = scene.add_cube(scn, gs.Matrix4.Identity, 0.1, 0.25, 0.1)
	boxes.append(box)

# main rendering loop
t = 0
while not input.key_press(gs.InputDevice.KeyEscape):
	# get the boxes dancing
	t += 0.0005

	for i, box in enumerate(boxes):
		t_ = t + i * 0.1
		pos = gs.Vector3(math.cos(t_), 0, math.sin(t_))
		rot = gs.Vector3(t_ * 2, t_ * -3, t_ + t * 4)
		box.GetTransform().SetWorld(gs.Matrix4.TransformationMatrix(pos, rot, gs.Vector3.One))

	# update the scene
	scn.Update()
	scn.WaitUpdate()

	scn.Commit()
	scn.WaitCommit()

	render.flip()
