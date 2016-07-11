# How to draw a primitive using the low-level renderer API
# For a more high-level example see the render_system tutorials

import os
import gs

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# create the renderer
egl = gs.EglRenderer()
egl.Open(480, 240)

# load a simple 2d shader outputting a single color
shader = egl.LoadShader(os.path.join(os.getcwd(), "../_data/shader_2d_color.isl"))

# Create index buffer
data = gs.BinaryBlob()
data.WriteShorts([0, 1, 2])

idx = egl.NewBuffer()
egl.CreateBuffer(idx, data, gs.GpuBuffer.Index)

# Create vertex buffer
vtx_layout = gs.VertexLayout()
vtx_layout.AddAttribute(gs.VertexAttribute.Position, 3, gs.ValueFloat)

data = gs.BinaryBlob()
x, y = 0.5, 0.5
data.WriteFloats([-x, -y, 0.5, -x, y, 0.5, x, y, 0.5])

vtx = egl.NewBuffer()
egl.CreateBuffer(vtx, data, gs.GpuBuffer.Vertex)

# draw loop
print("Close the renderer window or press Ctrl+C in this window to end")

while egl.GetDefaultOutputWindow():
	egl.Clear(gs.Color.Red)

	egl.SetShader(shader)
	egl.SetShaderFloat4("u_color", 0, 1, 0, 1)

	gs.DrawBuffers(egl, 3, idx, vtx, vtx_layout)

	egl.DrawFrame()
	egl.ShowFrame()

	egl.UpdateOutputWindow()
