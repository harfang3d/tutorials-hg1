-- How to read values from the mouse

hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(400, 300)

-- continue while the window is open
print("Click the left mouse button to print the current mouse cursor position")
print("Close the renderer window or press Ctrl+C in this window to end")

while (not plus:IsAppEnded()) do
	-- get the mouse device
	mouse_device = hg.GetInputSystem():GetDevice("mouse")

	-- check if left button is down
	if mouse_device:IsButtonDown(hg.Button0) then
		-- get the mouse position in the window ([0, 1])
		print(string.format("Mouse X: %f, Mouse Y: %f", mouse_device:GetValue(hg.InputAxisX), mouse_device:GetValue(hg.InputAxisY)))
    end
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()