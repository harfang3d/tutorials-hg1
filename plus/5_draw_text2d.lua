plus = gs.GetPlus()
plus:RenderInit(400, 300)

while not plus:KeyPress(gs.InputDevice.KeyEscape) do
	plus:Clear()
	plus:Text2D(120, 150, "Draw Text Example")
	plus:Flip()
end
