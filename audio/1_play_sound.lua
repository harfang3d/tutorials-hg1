-- Load an audio file as a static sound and replay it

gs.LoadPlugins()

-- mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

-- create an OpenAL mixer
al = gs.ALMixer()
al:Open()

-- load a sound
sound = al:LoadSound('../_data/good_evening.wav')

-- play the sound
channel = al:Start(sound)
print("Sound playing on channel: "..channel)

while al:GetPlayState(channel) == gs.MixerPlaying do
	gs.Sleep(1)
end
