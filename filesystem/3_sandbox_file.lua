hg = require("harfang")

-- Sand-boxed access to the file system

-- mount two std file driver under two different prefixes, only one acts as a sandbox
hg.MountFileDriver(hg.StdFileDriver(''), "std:")
hg.MountFileDriver(hg.StdFileDriver('', true), "box:")

-- access a data file outside of the std file driver root directory
std_path = "std:../_data/owl.jpg"
res_std_access = hg.GetFilesystem():Exists(std_path)

print("Can access '"..std_path.."' (expect OK): "..tostring(res_std_access))

-- do the same on the sandboxed mount point
box_path = "box:../_data/owl.jpg"
res_box_access = hg.GetFilesystem():Exists(box_path)

print("Can access '"..box_path.."' (expect KO): "..tostring(res_box_access))
