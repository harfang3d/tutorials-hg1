hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(400, 300)

while not plus:IsAppEnded() do
	plus:Clear()
	plus:Plot2D(200, 150, hg.Color.Green)
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()