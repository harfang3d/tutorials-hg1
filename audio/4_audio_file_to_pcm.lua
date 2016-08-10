-- Convert from any supported audio file format to a PCM file

gs.LoadPlugins()

gs.MountFileDriver(gs.StdFileDriver())

-- open input file as an audio data source
src = gs.GetAudioIO():Open('../_data/skaven.it')

-- open output file
out = gs.GetFilesystem():Open('skaven.pcm', gs.ModeWrite)

pcm = gs.BinaryBlob()

while not src:IsEOF() do
	-- get PCM frame to the binary blob
	size = src:GetFrame(pcm)
	-- output PCM frame to the file handle
	out:Write(pcm)
	-- reset the binary blob, do not free storage
	pcm:Reset()
end

-- - or - extract all PCM data to a huge binary blob and save it to file (consumes much more memory)

--[[
-- extract all PCM data from the source as a binary blob
sze, pcm = gs.ExtractAudioData(src)

-- save the complete PCM binary blob to a file
gs.GetFilesystem():FileSave('skaven.pcm'), pcm)
]]--
