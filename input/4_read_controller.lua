-- How to read values from a game controller

hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(400, 300)

device = hg.GetInputSystem():GetDevice("xinput.port0")

-- continue while the window is open
while (not plus:IsAppEnded()) do
	-- check if left button is down
    for i=hg.Button0,hg.ButtonLast do
		if device:WasButtonPressed(i) then
			print(string.format("%d was pressed",i))
        end
	end
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()