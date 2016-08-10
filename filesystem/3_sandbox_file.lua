-- Sand-boxed access to the file system

-- mount two std file driver under two different prefixes, only one acts as a sandbox
gs.MountFileDriver(gs.StdFileDriver(''), "std:")
gs.MountFileDriver(gs.StdFileDriver('', true), "box:")

-- access a data file outside of the std file driver root directory
std_path = "std:../_data/owl.jpg"
res_std_access = gs.GetFilesystem():Exists(std_path)

print("Can access '"..std_path.."': "..tostring(res_std_access))

-- do the same on the sandboxed mount point
box_path = "box:../_data/owl.jpg"
res_box_access = gs.GetFilesystem():Exists(box_path)

print("Can access '"..box_path.."': "..tostring(res_box_access))
