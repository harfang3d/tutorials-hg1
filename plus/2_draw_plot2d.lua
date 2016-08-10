plus = gs.GetPlus()
plus:RenderInit(400, 300)

while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	plus:Clear()
	plus:Plot2D(200, 150, gs.Color.Green)
	plus:Flip()
end