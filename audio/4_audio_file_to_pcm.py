# Convert from any supported audio file format to a PCM file

import gs
import os

gs.LoadPlugins(gs.get_default_plugins_path())

gs.MountFileDriver(gs.StdFileDriver())

# open input file as an audio data source
src = gs.GetAudioIO().Open(os.path.join(os.getcwd(), "../_data/skaven.it"))

# open output file
out = gs.GetFilesystem().Open(os.path.join(os.getcwd(), "skaven.pcm"), gs.ModeWrite)

pcm = gs.BinaryBlob()

while src.IsEOF() == False:
	# get PCM frame to the binary blob
	size = src.GetFrame(pcm)
	# output PCM frame to the file handle
	out.Write(pcm)
	# reset the binary blob, do not free storage
	pcm.Reset()

# - or - extract all PCM data to a huge binary blob and save it to file (consumes much more memory)

"""
# extract all PCM data from the source as a binary blob
sze, pcm = gs.ExtractAudioData(src)

# save the complete PCM binary blob to a file
gs.GetFilesystem().FileSave(os.path.join(os.getcwd(), "skaven.pcm"), pcm)
"""
