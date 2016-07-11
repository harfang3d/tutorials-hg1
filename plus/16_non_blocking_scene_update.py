"""
This tutorial displays two scene overlays:

- The background scene intentionally updates very slowly (it sleeps for 500ms).
- The foreground scene simply displays a spinning 3d cube.

Each scene is rendered to a different texture at a different rate. Both output
textures are drawn on top of each other to the screen as fast as possible.

Note that despite blocking Harfang's Lua VM the background scene does not block
rendering of the foreground scene and the main Python script execution.
"""

import gs
import gs.plus.render as render
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock
import time

gs.LoadPlugins(gs.get_default_plugins_path())
gs.MountFileDriver(gs.StdFileDriver("../_data/"), "@data/")

gs.plus.create_workers()

width, height = 640, 480
render.init(width, height, "../pkg.core")

renderer = render.get_renderer_async()


def create_slow_scene():
	scn = scene.new_scene()

	scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0, -10)))
	scene.add_light(scn, gs.Matrix4.RotationMatrix(gs.Vector3(0.6, -0.4, 0)), gs.Light.Model_Linear, 100, shadow=False)

	cube = scene.add_cube(scn, width=5)
	cube.AddComponent(gs.LogicScript("@data/spin_and_sleep.lua"))

	return scn


def update_slow_scene():
	while True:
		renderer.SetRenderTarget(rtt_slow)

		scn_slow.Update(gs.time(dt_sec))
		while not scn_slow.WaitUpdate(False):
			yield  # yield as long as the scene update is not complete

		scn_slow.Commit()
		while not scn_slow.WaitCommit(False):
			yield  # yield as long as the scene commit is not complete

		yield


def create_fast_scene():
	scn = scene.new_scene()

	scene.add_environment(scn, gs.Color.Transparent)  # clear color to transparent
	scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0, -10)))
	scene.add_light(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(6, 4, -6)))

	cube = scene.add_cube(scn)
	cube.AddComponent(gs.LogicScript("@data/spin.lua"))

	return scn


def update_fast_scene():
	renderer.SetRenderTarget(rtt_fast)

	scn_fast.Update(gs.time(dt_sec))
	scn_fast.WaitUpdate()
	scn_fast.Commit()
	scn_fast.WaitCommit()


def create_scene_render_target(w, h):
	tex = renderer.NewTexture()
	renderer.CreateTexture(tex, w, h)

	rtt = renderer.NewRenderTarget()
	renderer.CreateRenderTarget(rtt)
	renderer.SetRenderTargetColorTexture(rtt, tex)

	return rtt, tex


# create a render target for each scene
rtt_slow, tex_slow = create_scene_render_target(width, height)
rtt_fast, tex_fast = create_scene_render_target(width, height)

# create a slow scene and a fast scene
scn_slow = create_slow_scene()
scn_fast = create_fast_scene()

# start the slow scene co-routine
update_slow_scene_gen = update_slow_scene()

while not input.key_press(gs.InputDevice.KeyEscape):
	dt_sec = clock.update()

	# update the slow scene, the generator will return while Harfang works
	next(update_slow_scene_gen)

	# update the fast scene
	update_fast_scene()

	# composite the two scene output to screen
	renderer.SetRenderTarget(None)

	# render the slow scene output
	render.texture2d(0, 0, 1, tex_slow, flip_v=True)

	# composite the fast output using alpha blending
	render.set_blend_mode2d(render.BlendAlpha)
	render.texture2d(0, 0, 1, tex_fast, flip_v=True)

	# restore blend mode
	render.set_blend_mode2d(render.BlendOpaque)

	render.flip()
