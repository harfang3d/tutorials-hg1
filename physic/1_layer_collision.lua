-- Demonstrate how to prevent specific bodies from colliding with each other
hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(640, 400)

scn = plus:NewScene()
cam = plus:AddCamera(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1, -10)))
plus:AddLight(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(6, 4, -6)))
plus:AddPhysicCube(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(-3, 5, 0)))

-- add a plane in layer 0 (default layer)
plus:AddPhysicPlane(scn)

-- add 2 cubes in layer 1
node, rigid_body = plus:AddPhysicCube(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 5, 0)))
rigid_body:SetCollisionLayer(1)

node, rigid_body = plus:AddPhysicCube(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0.5, 2, 0.5)), 1, 1.5, 1)
rigid_body:SetCollisionLayer(1)

-- layer 1 collides with layer 0 but not with itself
scn:GetPhysicSystem():SetCollisionLayerPairState(0, 1, true)
scn:GetPhysicSystem():SetCollisionLayerPairState(1, 1, false)

fps = hg.FPSController(0, 2, -10)

while not plus:IsAppEnded() do
	dt_sec = plus:UpdateClock()

	fps:UpdateAndApplyToNode(cam, dt_sec)

	plus:UpdateScene(scn, dt_sec)
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()