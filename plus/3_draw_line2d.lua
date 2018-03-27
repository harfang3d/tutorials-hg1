hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(400, 300)

while not plus:IsAppEnded() do
	plus:Clear()
	plus:Line2D(0, 0, 400, 300, hg.Color.Red, hg.Color.Blue)
	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()