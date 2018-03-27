# Convert from any supported audio file format to a PCM file

import harfang as hg
import os

hg.LoadPlugins()

hg.MountFileDriver(hg.StdFileDriver())

# open input file as an audio data source
src = hg.GetAudioIO().Open('_data/skaven.it')

# open output file
out = hg.GetFilesystem().Open('skaven.pcm', hg.FileWrite)

pcm = hg.BinaryData()

while src.GetState() != hg.AudioDataEnded:
	# get PCM frame to the binary blob
	size, timestamp = src.GetFrame(pcm)
	# output PCM frame to the file handle
	out.Write(pcm)
	# reset the binary blob, do not free storage
	pcm.Reset()

# - or - extract all PCM data to a huge binary blob and save it to file (consumes much more memory)

"""
# extract all PCM data from the source as a binary blob
sze = hg.ExtractAudioData(src, pcm)

# save the complete PCM binary blob to a file
hg.GetFilesystem().FileSave(os.path.join(os.getcwd(), "skaven.pcm"), pcm)
"""

# Note: the pcm file can be played using vlc with the following command line:
# vlc --demux=rawaud --rawaud-channels=2 --rawaud-samplerate=44000 skaven.pcm