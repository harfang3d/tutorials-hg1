-- Access to a file inside a Zip archive
hg = require("harfang")

hg.LoadPlugins()

archive_path = '../_data/hello.zip'

-- mount a std file driver to access the archive
hg.MountFileDriver(hg.StdFileDriver())


-- mount a Zip file driver connected to the archive on the prefix "zip:"
file = hg.GetFilesystem():Open(archive_path, hg.FileRead)
hg.MountFileDriver(hg.ZipFileDriver(file), 'zip:')

-- assert that we can find a file named "hello.txt" on the "zip:" prefix
-- ie. inside the archive connected to the ZipFileDriver "zip:" resolves to
res = hg.GetFilesystem():Exists("zip:hello.txt")

print("Can access 'hello.txt' (expect OK): "..tostring(res))
