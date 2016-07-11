import gs

gs.GetFilesystem().Mount(gs.StdFileDriver("../pkg.core"), "@core")

gpu = gs.EglRenderer()
gpu.Open(640, 480)

gui = gs.GetDearImGui()

check = True
combo = 0
color = gs.Color(1, 0, 1)

while not gs.GetInputSystem().GetDevice("keyboard").WasPressed(gs.InputDevice.KeyEscape):
	gs.GetInputSystem().Update()

	if gui.Begin("GUI"):
		check = gui.Checkbox("Check", check)

		if gui.CollapsingHeader("Header", True, True):
			if gui.Button("Button"):
				print("Button pressed")

			combo = gui.Combo("Combo", ["Item 1", "Item 2", "Item 3"], combo)
			color = gui.ColorButton(color)
	gui.End()

	gpu.Clear(gs.Color.Red)
	gpu.DrawFrame()
	gpu.ShowFrame()

	gpu.UpdateOutputWindow()

gpu.Close()
