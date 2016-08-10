-- Stream an audio file using the OpenAL mixer

gs.LoadPlugins()

-- mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

-- create an OpenAL mixer
al = gs.ALMixer()
al:Open()

-- start streaming
channel = al:Stream('../_data/skaven.it')

-- wait until the user decides to exit the program or the stream ends
print('Playing on channel '..channel..', press Ctrl+C to stop.')

while al:GetPlayState(channel) == gs.MixerPlaying do
	gs.Sleep(1)
end
