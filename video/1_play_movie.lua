-- Movie playback with audio/video synchronization
--
-- Note: This sample is not performance oriented and does not represent
--		the most efficient way to replay a movie using the Harfang API.

hg = require("harfang")

hg.LoadPlugins()

hg.MountFileDriver(hg.StdFileDriver("_data/"), "@data")

width, height = 960, 540

-- initialize graphic and audio systems
plus = hg.GetPlus()
plus:RenderInit(width, height)
plus:AudioInit()

renderer = plus:GetRenderer()
mixer = plus:GetMixer()

-- open movie and retrieve video format
movie = hg.CreateMovie()
if not movie:Open(renderer, mixer, "@data/videoplayer-demo-harfang-60fps.webm") then
	print("Unsupported movie format")
end

-- load the YV12 to RGB shader and setup drawing states
shader = renderer:LoadShader("@data/yv12.isl")

-- create index buffer
data = hg.BinaryData()
data:WriteUInt16(0)
data:WriteUInt16(1)
data:WriteUInt16(2)
data:WriteUInt16(3)
data:WriteUInt16(4)
data:WriteUInt16(5)

idx = renderer:NewBuffer()
renderer:CreateBuffer(idx, data, hg.GpuBufferIndex)

-- Create vertex buffer
vtx_layout = hg.VertexLayout()
vtx_layout:AddAttribute(hg.VertexPosition, 3, hg.VertexFloat)
vtx_layout:AddAttribute(hg.VertexUV0, 2, hg.VertexFloat, true)

data = hg.BinaryData()
data:WriteFloats({0, 0, 0.5, 0, 1})
data:WriteFloats({0, height, 0.5, 0, 0})
data:WriteFloats({width, height, 0.5, 1, 0})
data:WriteFloats({0, 0, 0.5, 0, 1})
data:WriteFloats({width, height, 0.5, 1, 0})
data:WriteFloats({width, 0, 0.5, 1, 1})

vtx = renderer:NewBuffer()
renderer:CreateBuffer(vtx, data, hg.GpuBufferVertex)

renderer:EnableDepthTest(false) -- disable depth testing so that we don't even need to clear the screen

-- play until movie ends
movie:Play()
while not movie:IsEnded() and not plus:IsAppEnded() do
	plus:Clear(hg.Color.Red)
	
	renderer:SetViewport(hg.Rect(0, 0, width, height))
	renderer:Set2DMatrices() -- update the 2d matrices

	-- fetch the next video frame
	ok, frame = movie:GetFrame()
	-- draw the current video frame to screen
	if frame:size() then
		renderer:SetShader(shader)
		hg.SetShaderEngineValues(plus:GetRenderSystem())
		renderer:SetShaderTexture("y_tex", frame:at(0))
		renderer:SetShaderTexture("u_tex", frame:at(1))
		renderer:SetShaderTexture("v_tex", frame:at(2))
		hg.DrawBuffers(renderer, 6, idx, vtx, vtx_layout)
	end

	plus:Flip()
	plus:EndFrame()
end

movie:Close()
plus:AudioUninit()
plus:RenderUninit()
