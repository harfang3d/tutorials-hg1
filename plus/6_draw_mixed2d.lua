plus = gs.GetPlus()
plus:RenderInit(400, 300)

while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	plus:Clear()
	plus:Text2D(20, 200, "UNDER", 64)
	plus:Triangle2D(0 + 75, 150 - 50, 100 + 75, 300 - 50, 200 + 75, 150 - 50, gs.Color.Red, gs.Color.Blue, gs.Color.Green)
	plus:Line2D(0, 0, 400, 300)
	plus:Triangle2D(200 - 75, 0 + 50, 300 - 75, 150 + 50, 400 - 75, 0 + 50, gs.Color.Red, gs.Color.Blue, gs.Color.Green)
	plus:Text2D(200, 50, "OVER", 64)
	plus:SetBlend2D(gs.BlendAdditive)
	plus:Text2D(120, 135, "ADDITIVE", 32, gs.Color.Blue)
	plus:SetBlend2D(gs.BlendOpaque)
	plus:Flip()
end
