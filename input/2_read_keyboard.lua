-- How to read from the keyboard

hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(400, 300)

-- retrieve the keyboard device
keyboard = hg.GetInputSystem():GetDevice("keyboard")

print("Press 'X' to exit")

while not plus:IsAppEnded() do
	-- catch the exit key
	if keyboard:WasPressed(hg.KeyX) then
		break
    end
	-- log key presses
	for key=0,(hg.KeyLast-1) do
		if keyboard:WasPressed(key) then
            print(string.format("Keyboard key pressed: %d", key))
        end
    end
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()