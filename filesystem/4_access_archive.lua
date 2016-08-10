-- Access to a file inside a Zip archive

archive_path = '../_data/hello.zip'

-- mount a std file driver to access the archive
gs.MountFileDriver(gs.StdFileDriver())

-- mount a Zip file driver connected to the archive on the prefix "zip:"
gs.MountFileDriver(gs.ZipFileDriver(archive_path), 'zip:')

-- assert that we can find a file named "hello.txt" on the "zip:" prefix
-- ie. inside the archive connected to the ZipFileDriver "zip:" resolves to
res = gs.GetFilesystem():Exists("zip:hello.txt")

print("Can access 'hello.txt': "..tostring(res))
