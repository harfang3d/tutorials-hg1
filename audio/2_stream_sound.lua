-- Stream an audio file using the OpenAL mixer

hg = require("harfang")

hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- create a new mixer
mixer = hg.CreateMixer()
mixer:Open()

-- start streaming
channel = mixer:Stream('../_data/skaven.it')

-- wait until the user decides to exit the program or the stream ends
print('Playing on channel '..channel..', press Ctrl+C to stop.')

while mixer:GetPlayState(channel) == hg.MixerPlaying do
	hg.Sleep(hg.time_from_ms(100))
end

mixer:Close()