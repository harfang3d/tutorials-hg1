import gs
import gs.plus
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock
from math import pi, cos, sin, asin

gs.plus.create_workers()

render.init(1280, 720, "../pkg.core")

scn = scene.new_scene()
cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1.0, -15.0)))
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 150)
scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, pi, 0.2)), gs.Light.Model_Linear, diffuse=gs.Color(0.3, 0.3, 0.4))
scene.add_physic_plane(scn)

world = gs.Matrix4.TransformationMatrix(gs.Vector3(0, 5.0, 0), gs.Vector3(0, pi * 0.25, 0))
cube = scene.add_physic_cube(scn, world, 1, 1, 1, 2)

origin_node = gs.Node()
origin_node.AddComponent(gs.Transform())
origin_node.transform.SetPosition(gs.Vector3(0, 5.0, 0))
origin_node.AddComponent(gs.MakeRigidBody())
origin_node.AddComponent(gs.MakeBoxCollision())
# origin_rbody = gs.MakeRigidBody()
# origin_rbody.ResetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(0, 5.0, 0)), True)
# origin_node.AddComponent(origin_rbody)
origin_node.AddComponent(gs.Light())
scn.AddNode(origin_node)

joint = gs.MakeD6Joint()

for axis in [gs.D6JointAxis_X, gs.D6JointAxis_Y, gs.D6JointAxis_Z,
             gs.D6JointAxis_RotX, gs.D6JointAxis_RotY, gs.D6JointAxis_RotZ]:
	joint.SetAuthorizedAxis(axis, False)

joint.SetNodeA(cube[0])
joint.SetPivotA(gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0, 0)))
joint.SetNodeB(origin_node)
joint.SetPivotB(gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0, 0)))

cube[0].AddComponent(joint)
phase = 0.0

while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()
	phase += dt_sec
	scene.update_scene(scn, dt_sec)

	y = 2.5 + 2.0 * cos(phase * 3.0)
	# joint.SetPivotB(gs.Matrix4.TranslationMatrix(gs.Vector3(0, y, 0.0)))

	render.text2d(5, 25, "@%.2fFPS" % (1 / dt_sec))
	render.flip()
