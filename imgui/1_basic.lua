gpu = gs.EglRenderer()
gpu:Open(640, 480)

gui = gs.GetDearImGui()

check = true
combo = 0
color = gs.Color(1, 0, 1)

while not gs.GetKeyboard():WasPressed(gs.InputDevice.KeyEscape) do
	if gui:Begin("GUI") then
		check = gui:Checkbox("Check", check)

		if gui:CollapsingHeader("Header", true) then
			if gui:Button("Button") then
				print("Button pressed")
			end

			combo = gui:Combo("Combo", {"Item 1", "Item 2", "Item 3"}, combo)
			color = gui:ColorButton(color)
		end
	end

	gui:End()

	gpu:Clear(gs.Color.Red)
	gpu:DrawFrame()
	gpu:ShowFrame()

	gpu:UpdateOutputWindow()
end
