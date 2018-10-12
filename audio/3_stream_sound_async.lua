-- Demonstrates the use of the MixerAsync mixer interface wrapper

hg = require("harfang")

hg.LoadPlugins()

-- mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

-- create a new mixer and wrap it with the MixerAsync interface
mixer = hg.MixerAsync(hg.CreateMixer())
mixer:Open()

-- start streaming
future_channel = mixer:Stream('_data/skaven.it')

-- future_channel contains a FutureInt, this means that it will contain the channel the stream is playing on once the
-- mixer thread has executed the Stream call. the FutureInt get method blocks the caller until the value is available
-- and returns it.
channel = future_channel:get()

-- wait until the user decides to exit the program or the stream ends
print('Playing on channel '..channel..', press Ctrl+C to stop.')

while mixer:GetPlayState(channel):get() == hg.MixerPlaying do
	hg.Sleep(hg.time_from_ms(100))
end

mixer:Close()