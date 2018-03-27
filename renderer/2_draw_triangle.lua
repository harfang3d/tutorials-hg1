-- How to draw a primitive using the low-level renderer API
-- For a more high-level example see the render_system tutorials
hg = require("harfang")

-- load Harfang plugins (renderer, image loader, etc...)
hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- create the renderer
renderer = hg.CreateRenderer()
renderer:Open()

-- open a new window
win = hg.NewWindow(480, 240)

-- create a new output surface for the newly opened window
surface = renderer:NewOutputSurface(win)
renderer:SetOutputSurface(surface)

-- load a simple 2d shader outputting a single color
shader = renderer:LoadShader("_data/shader_2d_color.isl")

-- create index buffer
data = hg.BinaryData()
data:WriteUInt16s({0,1,2})

idx = renderer:NewBuffer()
renderer:CreateBuffer(idx, data, hg.GpuBufferIndex)

-- Create vertex buffer
vtx_layout = hg.VertexLayout()
vtx_layout:AddAttribute(hg.VertexPosition, 3, hg.VertexFloat)

data = hg.BinaryData()

x, y = 0.5, 0.5
data:WriteFloats({-x,-y, 0.5})
data:WriteFloats({-x, y, 0.5})
data:WriteFloats({ x, y, 0.5})

vtx = renderer:NewBuffer()
renderer:CreateBuffer(vtx, data, hg.GpuBufferVertex)

-- get keyboard device
keyboard = hg.GetInputSystem():GetDevice("keyboard")

-- draw loop
print("Close the renderer window or press Ctrl+C in this window to end")

while hg.IsWindowOpen(win) and (not keyboard:WasPressed(hg.KeyEscape)) do
	renderer:Clear(hg.Color.Red)

	renderer:SetShader(shader)
	renderer:SetShaderFloat4("u_color", 0, 1, 0, 1)

	hg.DrawBuffers(renderer, 3, idx, vtx, vtx_layout)

	renderer:DrawFrame()
	renderer:ShowFrame()

	hg.UpdateWindow(win)

	hg.EndFrame()
end

renderer:DestroyOutputSurface(surface)
hg.DestroyWindow(win)
renderer:Close()
