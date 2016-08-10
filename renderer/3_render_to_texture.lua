-- How to draw to a texture using the low-level renderer API

-- mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

-- create the renderer
egl = gs.EglRenderer()
egl:Open(640, 480)

-- load 2d shader and retrieve variables
shader_color = egl:LoadShader("../_data/shader_2d_color.isl")
shader_texture = egl:LoadShader("../_data/shader_2d_single_texture.isl")

-- create primitive index buffer
data = gs.BinaryBlob()
data:WriteShorts({0, 1, 2})

idx = egl:NewBuffer()
egl:CreateBuffer(idx, data, gs.GpuBuffer.Index)

-- create primitive vertex buffer
vtx_layout = gs.VertexLayout()
vtx_layout:AddAttribute(gs.VertexAttribute.Position, 3, gs.ValueFloat)
vtx_layout:AddAttribute(gs.VertexAttribute.UV0, 2, gs.ValueUByte, true) -- UVs are sent as normalized 8 bit unsigned integer (range [0;255])

data = gs.BinaryBlob()
x, y = 0.5, 0.5
data:WriteFloats({-x, -y, 0.5})
data:WriteUnsignedBytes({127, 0})
data:WriteFloats({-x, y, 0.5})
data:WriteUnsignedBytes({0, 127})
data:WriteFloats({x, y, 0.5})
data:WriteUnsignedBytes({127, 127})

vtx = egl:NewBuffer()
egl:CreateBuffer(vtx, data, gs.GpuBuffer.Vertex)

-- create the texture we will render to
tgt_tex = egl:NewTexture()
egl:CreateTexture(tgt_tex, 64, 64)

-- create and configure the frame buffer object to render to the texture
tgt_rt = egl:NewRenderTarget()
egl:CreateRenderTarget(tgt_rt)
egl:SetRenderTargetColorTexture(tgt_rt, tgt_tex)

-- draw loop
print("Close the renderer window or press Ctrl+C in this window to end")

while egl:GetDefaultOutputWindow() ~= nil do
	-- first render a blue triangle on a green background to the texture using the
	-- render target
	egl:SetRenderTarget(tgt_rt)

	egl:SetViewport(gs.fRect(0, 0, 64, 64)) -- fit viewport to texture dimensions
	egl:Clear(gs.Color.Green)

	egl:SetShader(shader_color)
	egl:SetShaderFloat4("u_color", 0, 0, 1, 1) -- blue
	gs.DrawBuffers(egl, 3, idx, vtx, vtx_layout)

	-- switch back to the default render target and display the texture we just
	-- rendered to using a triangle on a red background

	-- note that the UVs are skewed so that the triangle drawn into the texture
	-- does not exactly overlap with the triangle used to display the texture
	egl:SetRenderTarget(nil)

	local window_size = egl:GetDefaultOutputWindow():GetSize()
	egl:SetViewport(gs.fRect(0, 0, window_size.x, window_size.y)) -- fit viewport to window dimensions
	egl:Clear(gs.Color.Red)

	egl:SetShader(shader_texture)
	egl:SetShaderTexture("u_tex", tgt_tex)
	gs.DrawBuffers(egl, 3, idx, vtx, vtx_layout)

	egl:DrawFrame()
	egl:ShowFrame()

	egl:UpdateOutputWindow()
end
