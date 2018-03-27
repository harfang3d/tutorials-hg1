-- create a chain of rigid bodies connected by spherical joints
hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(1280, 720)

scn = plus:NewScene()
scn:GetPhysicSystem():SetDebugVisuals(true)

cam = plus:AddCamera(scn, hg.Matrix4.TransformationMatrix(hg.Vector3(0, 30, -30), hg.Vector3(0.7, 0, 0)))
plus:AddLight(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 20, -7)), hg.LightModelPoint)
plus:AddPhysicPlane(scn)

function create_chain(nb_link)
	local function create_link(node)
		local other_node, other_body = plus:AddPhysicSphere(scn, hg.Matrix4.TranslationMatrix(
			node:GetTransform():GetPosition() + hg.Vector3(1, 0, 0)), 0.5, 6, 16, 10)

		local joint = hg.SphericalJoint()
		joint:SetOtherBody(other_node)
		joint:SetPivot(hg.Vector3(0.5, 0, 0))
		joint:SetOtherPivot(hg.Vector3(-0.5, 0, 0))
		node:AddComponent(joint)

		return other_node
	end

	local root_node, root_body = plus:AddPhysicSphere(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 14, 0)), 0.5, 6, 16, 0)
	root_body:SetType(hg.RigidBodyKinematic)
	root_body:SetIsSleeping(true)

	local current_node = root_node
	for i = 1, nb_link do
		current_node = create_link(current_node)
	end

	return root_node, root_body
end

root_node, root_body = create_chain(10)

while not plus:IsAppEnded() do
	local dt = plus:UpdateClock()
	plus:UpdateScene(scn, dt)
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()
