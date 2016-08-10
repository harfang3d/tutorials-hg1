-- Access to the file system

-- mount the system file driver, StdFileDriver wraps the system native file API
gs.MountFileDriver(gs.StdFileDriver())

-- test that we indeed have access to the file system
path = '../_data/owl.jpg' -- relative path to a file on the file system
result = gs.GetFilesystem():Exists(path) -- can the engine file system see it?

print("Access OK: "..tostring(result))
