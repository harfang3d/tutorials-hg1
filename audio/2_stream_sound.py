# Stream an audio file using the OpenAL mixer

import os
import gs
import time

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# create an OpenAL mixer
al = gs.ALMixer()
al.Open()

# start streaming
channel = al.Stream(os.path.join(os.getcwd(), "../_data/skaven.it"))

# wait until the user decides to exit the program or the stream ends
print("Playing on channel %d, press Ctrl+C to stop." % channel)

while al.GetPlayState(channel) == gs.MixerPlaying:
	time.sleep(0.1)
