-- Demonstrates the use of the MixerAsync mixer interface wrapper

gs.LoadPlugins()

-- mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

-- create an OpenAL mixer and wrap it with the MixerAsync interface
al = gs.MixerAsync(gs.ALMixer())
al:Open()

-- start streaming
future_channel = al:Stream('../_data/skaven.it')

-- future_channel contains a FutureInt, this means that it will contain the channel the stream is playing on once the
-- mixer thread has executed the Stream call. the FutureInt get method blocks the caller until the value is available
-- and returns it.
channel = future_channel:get()

-- wait until the user decides to exit the program or the stream ends
print('Playing on channel '..channel..', press Ctrl+C to stop.')

while al:GetPlayState(channel):get() == gs.MixerPlaying do
	gs.Sleep(1)
end
