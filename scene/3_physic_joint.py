# Create a chain of rigid bodies connected by spherical joints

import gs

gs.LoadPlugins()

plus = gs.GetPlus()
plus.RenderInit(1280, 720)

scn = plus.NewScene()
scn.GetPhysicSystem().SetDebugVisuals(True)

cam = plus.AddCamera(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(0, 30, -30), gs.Vector3(0.7, 0, 0)))
plus.AddLight(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 20, -7)), gs.Light.Model_Point)
plus.AddPhysicPlane(scn)


def create_chain(nb_link):
	def create_link(node):
		other_node, other_body = plus.AddPhysicSphere(scn, gs.Matrix4.TranslationMatrix(
			node.GetComponent("Transform").GetPosition() + gs.Vector3(1, 0, 0)), 0.5, 6, 16, 10)

		joint = gs.MakeSphericalJoint()
		joint.SetOtherBody(other_node)
		joint.SetPivot(gs.Vector3(0.5, 0, 0))
		joint.SetOtherPivot(gs.Vector3(-0.5, 0, 0))
		node.AddComponent(joint)

		return other_node

	root_node, root_body = plus.AddPhysicSphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 14, 0)), 0.5, 6, 16, 0)
	root_body.SetType(gs.RigidBodyKinematic)
	root_body.SetIsSleeping(True)

	current_node = root_node
	for i in range(nb_link):
		current_node = create_link(current_node)

	return root_node, root_body


root_node, root_body = create_chain(10)

while not plus.KeyPress(gs.InputDevice.KeyEscape):
	dt = plus.UpdateClock()
	plus.UpdateScene(scn, dt)
	plus.Flip()
