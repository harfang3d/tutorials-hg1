# Stream an audio file using the OpenAL mixer

import harfang as hg

hg.LoadPlugins()

# mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

# create a new mixer
mixer = hg.CreateMixer()
mixer.Open()

# start streaming
channel = mixer.Stream("_data/skaven.it")

# wait until the user decides to exit the program or the stream ends
print("Playing on channel %d, press Ctrl+C to stop." % channel)

while mixer.GetPlayState(channel) == hg.MixerPlaying:
	hg.Sleep(hg.time_from_ms(100))

mixer.Close()