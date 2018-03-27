# Load an audio file as a static sound and replay it

import harfang as hg

hg.LoadPlugins()

# mount the system file driver
hg.MountFileDriver(hg.StdFileDriver())

# create a new sound mixer
mixer = hg.CreateMixer()
mixer.Open()

# load a sound
sound = mixer.LoadSound("_data/good_evening.wav")

# play the sound
channel = mixer.Start(sound)
print("Sound playing on channel: %d" % channel)

while mixer.GetPlayState(channel) == hg.MixerPlaying:
	hg.Sleep(hg.time_from_ms(100))

mixer.Close()