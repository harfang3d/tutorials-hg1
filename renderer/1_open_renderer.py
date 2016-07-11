# Initialize the renderer

import gs

egl = gs.EglRenderer()
egl.Open(480, 240)

print("Close the renderer window or press Ctrl+C in this window to end")

while egl.GetDefaultOutputWindow():
	egl.Clear(gs.Color.Red)
	egl.ShowFrame()
	egl.UpdateOutputWindow()
