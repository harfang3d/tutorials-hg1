hg = require("harfang")

hg.LoadPlugins()

plus = hg.GetPlus()
plus:RenderInit(400, 300)

while not plus:IsAppEnded() do
	plus:Flip()
	plus:EndFrame()
end
