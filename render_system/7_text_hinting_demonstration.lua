-- Demonstrate the effect of hinting and grid snapping on text rendering with raster font

hg = require("harfang")

hg.LoadPlugins()

-- create the renderer
renderer = hg.CreateRenderer()
renderer:Open()

-- open a new window
win = hg.NewWindow(1000, 1000)

-- create a new output surface for the newly opened window
surface = renderer:NewOutputSurface(win)
renderer:SetOutputSurface(surface)

-- initialize the render system, which is used to draw through the renderer
render_system = hg.RenderSystem()
render_system:Initialize(renderer)

-- create the font objects
no_hint_fonts = {}
for size=4,43 do
	table.insert(no_hint_fonts, hg.RasterFont("@core/fonts/default.ttf", size, 512))
end
hint_fonts = {}
for size=4,43 do
	table.insert(hint_fonts,hg.RasterFont("@core/fonts/default.ttf", size, 512, 2, true))
end
-- set default render states
renderer:Set2DMatrices()
renderer:EnableBlending(true)
renderer:EnableDepthTest(false)

hinting = false
glyph_snap = true

-- retrieve the keyboard device
keyboard = hg.GetInputSystem():GetDevice("keyboard")

while hg.IsWindowOpen(win) and (not keyboard:WasPressed(hg.KeyEscape)) do
	renderer:Clear(hg.Color.Black)

	-- catch key press
	if keyboard:WasPressed(hg.KeyNumpad1) then
        hinting = not hinting
    end
	if keyboard:WasPressed(hg.KeyNumpad2) then
		glyph_snap = not glyph_snap
    end
	-- display instructions
	no_hint_fonts[12]:Write(render_system, "Press 1 to toggle hinting, 2 to toggle glyph snap", hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1000 - 16, 0.5)))
	no_hint_fonts[12]:Write(render_system, string.format("Hinting: %s", tostring(hinting)), hg.Matrix4.TranslationMatrix(hg.Vector3(40, 1000 - 36, 0.5)), hinting and hg.Color.Green or hg.Color.Red)
	no_hint_fonts[12]:Write(render_system, string.format("Glyph snap: %s", tostring(glyph_snap)), hg.Matrix4.TranslationMatrix(hg.Vector3(230, 1000 - 36, 0.5)), glyph_snap and hg.Color.Green or hg.Color.Red)

	-- display the list of fonts
	cursor = hg.Vector3(0, 10, 0.5)
	for _,font in pairs(hinting and hint_fonts or no_hint_fonts) do
		rect = font:GetTextRect(render_system, "ABCDEFGHIJKLMNOPQRSTUVWXYZ - VA")
		font:Write(render_system, "ABCDEFGHIJKLMNOPQRSTUVWXYZ - VA", hg.Matrix4.TranslationMatrix(cursor), hg.Color.White, 1, glyph_snap, true)
        cursor.y = cursor.y + rect:GetHeight()
    end
	render_system:DrawRasterFontBatch()

	renderer:DrawFrame()
	renderer:ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()
end
font = None
