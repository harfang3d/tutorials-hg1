plus = gs.GetPlus()
plus:RenderInit(400, 300)

while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	plus:Clear()
	plus:Line2D(0, 0, 400, 300, gs.Color.Red, gs.Color.Blue)
	plus:Flip()
end
