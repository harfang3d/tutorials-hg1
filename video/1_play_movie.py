# Movie playback with audio/video synchronization
#
# Note: This sample is not performance oriented and does not represent
#		the most efficient way to replay a movie using the Harfang API.

import gs

gs.MountFileDriver(gs.StdFileDriver("../_data/"), "@data")

# initialize graphic and audio systems
al = gs.ALMixer()
al.Open()

gpu = gs.EglRenderer()
gpu.Open(960, 540)

render_system = gs.RenderSystem()
render_system.Initialize(gpu)

# open movie and retrieve video format
movie = gs.WebMMovie()
if not movie.Open("@data/film_blender_ToS-4k-1920.webm"):
	print("Unsupported movie format")

video_format = movie.GetVideoData().GetFormat()

# create the frame textures and frame object
y_tex = gpu.NewTexture()
gpu.CreateTexture(y_tex, video_format.width, video_format.height, gs.GpuTexture.R8, gs.GpuTexture.NoAA, gs.GpuTexture.UsageDefault, False)
u_tex = gpu.NewTexture()
gpu.CreateTexture(u_tex, video_format.width // 2, video_format.height // 2, gs.GpuTexture.R8, gs.GpuTexture.NoAA, gs.GpuTexture.UsageDefault, False)
v_tex = gpu.NewTexture()
gpu.CreateTexture(v_tex, video_format.width // 2, video_format.height // 2, gs.GpuTexture.R8, gs.GpuTexture.NoAA, gs.GpuTexture.UsageDefault, False)

frame = gs.VideoFrame()
video_format.ClearFrame(frame)
video_timestamp = gs.time(0)  # assume first frame time stamp is 0

# load the YV12 to RGB shader and setup drawing states
shader = gpu.LoadShader("@data/yv12.isl")

gpu.EnableDepthTest(False)  # disable depth testing so that we don't even need to clear the screen

# start streaming the movie audio data
channel = al.StreamData(movie.GetAudioData())

# play until movie ends
while not movie.IsEOF() and not gs.GetKeyboard().WasPressed(gs.InputDevice.KeyEscape):
	# fit the while output window
	screen_size = gpu.GetCurrentOutputWindow().GetSize()
	gpu.SetViewport(gs.fRect(0, 0, screen_size.x, screen_size.y))
	gpu.Set2DMatrices()  # update the 2d matrix

	# fetch the next video frame once audio gets past video
	audio_timestamp = al.GetChannelPosition(channel)  # audio timestamp as reported by the mixer

	if audio_timestamp >= video_timestamp:
		movie.GetVideoData().GetFrame(frame)
		video_timestamp = frame.GetTimestamp()
		gpu.BlitTexture(y_tex, frame.GetPlaneData(gs.VideoFrame.Y), video_format.width, video_format.height)
		gpu.BlitTexture(u_tex, frame.GetPlaneData(gs.VideoFrame.U), video_format.width // 2, video_format.height // 2)
		gpu.BlitTexture(v_tex, frame.GetPlaneData(gs.VideoFrame.V), video_format.width // 2, video_format.height // 2)

	# draw the current video frame to screen
	vtxs = [gs.Vector3(0, 0, 0.5), gs.Vector3(0, screen_size.y, 0.5), gs.Vector3(screen_size.x, screen_size.y, 0.5), gs.Vector3(0, 0, 0.5), gs.Vector3(screen_size.x, screen_size.y, 0.5), gs.Vector3(screen_size.x, 0, 0.5)]
	uvs = [gs.Vector2(0, 1), gs.Vector2(0, 0), gs.Vector2(1, 0), gs.Vector2(0, 1), gs.Vector2(1, 0), gs.Vector2(1, 1)]

	gpu.SetShader(shader)
	gs.SetShaderEngineValues(render_system)
	gpu.SetShaderTexture("y_tex", y_tex)
	gpu.SetShaderTexture("u_tex", u_tex)
	gpu.SetShaderTexture("v_tex", v_tex)
	render_system.DrawTriangleUV(2, vtxs, uvs)

	gpu.DrawFrame()
	gpu.ShowFrame()
	gpu.UpdateOutputWindow()
