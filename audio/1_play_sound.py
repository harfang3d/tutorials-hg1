# Load an audio file as a static sound and replay it

import os
import gs
import time

gs.LoadPlugins()

# mount the system file driver
gs.MountFileDriver(gs.StdFileDriver())

# create an OpenAL mixer
al = gs.ALMixer()
al.Open()

# load a sound
sound = al.LoadSound(os.path.join(os.getcwd(), "../_data/good_evening.wav"))

# play the sound
channel = al.Start(sound)
print("Sound playing on channel: %d" % channel)

while al.GetPlayState(channel) == gs.MixerPlaying:
	time.sleep(0.1)  # pause until the sound is done playing
