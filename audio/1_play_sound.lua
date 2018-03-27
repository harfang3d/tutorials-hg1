-- Load an audio file as a static sound and replay it

hg = require("harfang")

hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- create a new sound mixer
mixer = hg.CreateMixer()
mixer:Open()

-- load a sound
sound = mixer:LoadSound("../_data/good_evening.wav")

-- play the sound
channel = mixer:Start(sound)
print("Sound playing on channel: "..channel)

while mixer:GetPlayState(channel) == hg.MixerPlaying do
	hg.Sleep(hg.time_from_ms(100))
end

mixer:Close()