import gs
import math

# create a few bench objects
bench_fill_field = []
bench_polygonise = []
bench_create_geo = []

# setup iso field
w, h, d = 100, 60, 30

field = gs.BinaryBlob()
field.Grow(w * h * d)
for i in range(w * h * d):
	field.WriteFloat(0)

iso = gs.IsoSurface()


def draw_bench(perf_hist, color):
	size = len(perf_hist)

	while size > (257):
		perf_hist.pop(0)
		size -= 1

	k_x = 1280 / 256  # display all values on screen
	k_y = 720 / (16 * 1000)  # y goes up to 16ms
	for i in range(size - 1):
		plus.Line2D(i * k_x, perf_hist[i] * k_y, (i + 1) * k_x, perf_hist[i + 1] * k_y, color, color)

	plus.Text2D(1280 - 80, perf_hist[-1] * k_y + 10, "%.2f ms" % (perf_hist[-1] / 1000), 16, color)


def update_field(a):
	def write_to_field(x, y, z, v):
		x, y, z = int(x), int(y), int(z)
		o = (w * d * y + w * z + x) * 4
		field.WriteFloatAt(v, o)

	t_ref = gs.time.now_us()
	for i in range(0, 200):
		a_rad = i * (math.pi / 180) * 2

		x = (math.sin(a_rad * -0.75 + a * 1.2) * math.cos(a_rad * 1.50 + a * -1.2) * 0.45 + 0.5) * w
		y = (math.cos(a_rad * 1.00 + a * -2.0) * math.sin(a_rad * 1.25 + a * 1.8) * 0.45 + 0.5) * h
		z = (math.sin(a_rad * 1.40 + a * 1.5) * math.cos(a_rad * -0.75 + a * -2.5) * 0.45 + 0.5) * d

		write_to_field(x, y, z, 6)

	gs.BinaryBlobBlur3d(field, w, h, d)

	t_new = gs.time.now_us()
	bench_fill_field.append(t_new - t_ref)

	# polygonise
	t_ref = t_new

	iso.Clear(False)  # keep storage to minimize heap allocations
	gs.PolygoniseIsoSurface(w, h, d, field, 1, iso)

	t_new = gs.time.now_us()
	bench_polygonise.append(t_new - t_ref)

	# convert to render geometry
	t_ref = t_new

	if False:  # slow path through core geometry
		geo = gs.CoreGeometry()
		gs.IsoSurfaceToCoreGeometry(iso, geo)
		geo = plus.CreateGeometry(geo, False)
	else:
		geo = gs.RenderGeometry()
		gs.IsoSurfaceToRenderGeometry(plus.GetRenderSystem(), iso, geo, mat)

	t_new = gs.time.now_us()
	bench_create_geo.append(t_new - t_ref)

	return geo

#
gs.MountFileDriver(gs.StdFileDriver("../_data/"), "@data/")

plus = gs.GetPlus()
plus.RenderInit(1280, 720)

mat = plus.LoadMaterial("@core/materials/default.mat")
fps = gs.FPSController(w / 2, h / 2, -100)

#
scn = plus.NewScene()
cam = plus.AddCamera(scn, gs.Matrix4.TranslationMatrix((0, 1, -10)))
plus.AddLight(scn, gs.Matrix4.RotationMatrix((0.6, -0.4, 0)), gs.Light.Model_Linear, 300)
plus.AddPlane(scn)

renderable_system = scn.GetRenderableSystem()

a = 0
while not plus.KeyPress(gs.InputDevice.KeyEscape):
	dt = plus.UpdateClock()
	fps.UpdateAndApplyToNode(cam, dt)

	geo = update_field(a)
	a += dt.to_sec() * 0.5

	renderable_system.DrawGeometry(geo, gs.Matrix4.Identity)

	plus.UpdateScene(scn, dt)

	draw_bench(bench_fill_field, gs.Color.Red)
	draw_bench(bench_polygonise, gs.Color.Green)
	draw_bench(bench_create_geo, gs.Color.Blue)

	plus.Text2D(800, 45, "Update scalar field", 16, gs.Color.Red)
	plus.Text2D(800, 25, "Polygonise scalar field", 16, gs.Color.Green)
	plus.Text2D(800, 5, "Prepare render geometry", 16, gs.Color.Blue)

	plus.Text2D(5, 25, "Iso-surface @%.2fFPS (%d triangle)" % (1 / dt.to_sec(), iso.GetTriangleCount()))
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around")

	plus.Flip()
