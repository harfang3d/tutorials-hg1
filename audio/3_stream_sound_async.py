# Demonstrates the use of the MixerAsync mixer interface wrapper

import os
import gs
import time

gs.LoadPlugins(gs.get_default_plugins_path())

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# create an OpenAL mixer and wrap it with the MixerAsync interface
al = gs.MixerAsync(gs.ALMixer())
al.Open()
future_channel = al.Stream(os.path.join(os.getcwd(), "../_data/skaven.it"))

# future_channel contains a FutureInt, this means that it will contain the channel the stream is playing on once the
# mixer thread has executed the Stream call. the FutureInt get method blocks the caller until the value is available
# and returns it.
channel = future_channel.get()

# wait until the user decides to exit the program or the stream ends
print("Playing on channel %d, press Ctrl+C to stop." % channel)

while al.GetPlayState(channel).get() == gs.MixerPlaying:
	time.sleep(0.1)
