hg = require("harfang")

hg.LoadPlugins()

-- create a few bench objects
bench_fill_field = {}
bench_polygonise = {}
bench_create_geo = {}

-- setup iso field
w, h, d = 100, 60, 30

field = hg.BinaryData()
field:Grow(w * h * d)
for i = 1, w * h * d do
	field:WriteFloat(0)
end

iso = hg.IsoSurface()

function draw_bench(perf_hist, color)
	local size = #perf_hist

	while size > 257 do
		table.remove(perf_hist, 1)
		size = size - 1
	end

	local k_x = 1280 / 256 -- display all values on screen
	local k_y = 720 / (16 * 1000) -- y goes up to 16ms
	for i = 1, size - 1 do
		plus:Line2D(i * k_x, perf_hist[i] * k_y, (i + 1) * k_x, perf_hist[i + 1] * k_y, color, color)
	end

	plus:Text2D(1280 - 80, perf_hist[#perf_hist] * k_y + 10, string.format("%.2f ms", perf_hist[#perf_hist] / 1000), 16, color)
end

function update_field(a)
	function write_to_field(x, y, z, v)
		local x, y, z = math.floor(x), math.floor(y), math.floor(z)
		local o = (w * d * y + w * z + x) * 4
		field:WriteFloatAt(v, o)
	end

	local t_ref = hg.time_to_us_f(hg.time_now())
	for i = 1, 200 do
		local a_rad = i * (math.pi / 180) * 2

		local x = (math.sin(a_rad * -0.75 + a * 1.2) * math.cos(a_rad * 1.50 + a * -1.2) * 0.45 + 0.5) * w
		local y = (math.cos(a_rad * 1.00 + a * -2.0) * math.sin(a_rad * 1.25 + a * 1.8) * 0.45 + 0.5) * h
		local z = (math.sin(a_rad * 1.40 + a * 1.5) * math.cos(a_rad * -0.75 + a * -2.5) * 0.45 + 0.5) * d

		write_to_field(x, y, z, 6)
	end

	hg.BinaryDataBlur3d(field, w, h, d)

	local t_new = hg.time_to_us_f(hg.time_now())
	table.insert(bench_fill_field, t_new - t_ref)

	-- polygonise
	t_ref = t_new

	iso:Clear()
	hg.PolygoniseIsoSurface(w-2, h-2, d-2, field, 1, iso)

	t_new = hg.time_to_us_f(hg.time_now())
	table.insert(bench_polygonise, t_new - t_ref)

	-- convert to render geometry
	t_ref = t_new

	local geo
	if false then -- slow path through core geometry
		geo = hg.CoreGeometry()
		hg.IsoSurfaceToCoreGeometry(iso, geo)
		geo = plus:CreateGeometry(geo, false)
	else
		geo = hg.RenderGeometry()
		hg.IsoSurfaceToRenderGeometry(plus:GetRenderSystem(), iso, geo, mat)
	end

	t_new = hg.time_to_us_f(hg.time_now())
	table.insert(bench_create_geo, t_new - t_ref)

	return geo
end

--
hg.MountFileDriver(hg.StdFileDriver("../_data/"), "@data/")

plus = hg.GetPlus()
plus:RenderInit(1280, 720)

mat = plus:LoadMaterial("@core/materials/default.mat")
fps = hg.FPSController(w / 2, h / 2, -100)

--
scn = plus:NewScene()
cam = plus:AddCamera(scn, hg.Matrix4.TranslationMatrix(hg.Vector3(0, 1, -10)))
plus:AddLight(scn, hg.Matrix4.RotationMatrix(hg.Vector3(0.6, -0.4, 0)), hg.LightModelLinear, 300)
plus:AddPlane(scn)

renderable_system = scn:GetRenderableSystem()

a = 0
while not plus:IsAppEnded() do
	local dt = plus:UpdateClock()
	fps:UpdateAndApplyToNode(cam, dt)

	local geo = update_field(a)
	a = a + hg.time_to_sec_f(dt) * 0.5

	renderable_system:DrawGeometry(geo, hg.Matrix4.Identity)

	plus:UpdateScene(scn, dt)

	draw_bench(bench_fill_field, hg.Color.Red)
	draw_bench(bench_polygonise, hg.Color.Green)
	draw_bench(bench_create_geo, hg.Color.Blue)

	plus:Text2D(800, 45, "Update scalar field", 16, hg.Color.Red)
	plus:Text2D(800, 25, "Polygonise scalar field", 16, hg.Color.Green)
	plus:Text2D(800, 5, "Prepare render geometry", 16, hg.Color.Blue)

	plus:Text2D(5, 25, string.format("Iso-surface @%.2fFPS (%d triangle)", 1 / hg.time_to_sec_f(dt), iso:GetTriangleCount()))
	plus:Text2D(5, 5, "Move around with QSZD, left mouse button to look around")

	plus:Flip()
	plus:EndFrame()
end

plus:RenderUninit()