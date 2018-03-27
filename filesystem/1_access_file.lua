hg = require("harfang")

-- Access to the file system

-- mount the system file driver, StdFileDriver wraps the system native file API
hg.MountFileDriver(hg.StdFileDriver())

-- test that we indeed have access to the file system
path = '../_data/owl.jpg' -- relative path to a file on the file system
result = hg.GetFilesystem():Exists(path) -- can the engine file system see it?

print("Access OK: "..tostring(result))
