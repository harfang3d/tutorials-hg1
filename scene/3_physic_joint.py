# Create a chain of rigid bodies connected by spherical joints

import gs
import gs.plus.render as render
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock
import math

gs.LoadPlugins(gs.get_default_plugins_path())
render.init(1024, 768, "../pkg.core")

scn = scene.new_scene()
scn.GetPhysicSystem().SetDebugVisuals(True)

cam = scene.add_camera(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(0, 30, -30), gs.Vector3(0.7, 0, 0)))
scene.add_light(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 20, -7)), gs.Light.Model_Point)
scene.add_physic_plane(scn)


def create_chain(nb_link):
	def create_link(node):
		other_node, other_body = scene.add_physic_sphere(scn, gs.Matrix4.TranslationMatrix(
			node.GetComponent("Transform").GetPosition() + gs.Vector3(1, 0, 0)), mass=10)

		joint = gs.MakeSphericalJoint()
		joint.SetOtherBody(other_node)
		joint.SetPivot(gs.Vector3(0.5, 0, 0))
		joint.SetOtherPivot(gs.Vector3(-0.5, 0, 0))
		node.AddComponent(joint)

		return other_node

	root_node, root_body = scene.add_physic_sphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 14, 0)), mass=0)
	root_body.SetType(gs.RigidBodyKinematic)
	root_body.SetIsSleeping(True)

	current_node = root_node
	for i in range(nb_link):
		current_node = create_link(current_node)

	return root_node, root_body


root_node, root_body = create_chain(10)

while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()
	t = clock.get()

	#root_node.GetTransform().SetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(math.cos(t) * 3, 10, math.sin(t) * 3)))

	scene.update_scene(scn, dt_sec)

	render.flip()
