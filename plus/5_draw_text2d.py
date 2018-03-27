import harfang as hg

hg.LoadPlugins()

plus = hg.GetPlus()
plus.RenderInit(400, 300)

while not plus.IsAppEnded():
	plus.Clear()
	plus.Text2D(120, 150, "Draw Text Example")
	plus.Flip()
	plus.EndFrame()

plus.RenderUninit()