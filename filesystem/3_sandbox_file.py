# Sand-boxed access to the file system

import os
import gs

# mount two std file driver under two different prefixes, only one acts as a sandbox
gs.MountFileDriver(gs.StdFileDriver(os.path.dirname(__file__)), "std:")
gs.MountFileDriver(gs.StdFileDriver(os.path.dirname(__file__), True), "box:")

# access the readme.txt file outside of the std file driver root directory:
std_path = "std:../readme.txt"
res_std_access = gs.GetFilesystem().Exists(std_path)

# do the same on the sandboxed box: mount point
box_path = "box:../readme.txt"
res_box_access = gs.GetFilesystem().Exists(box_path)

print("Can access '%s': %s" % (std_path, str(res_std_access)))
print("Can access '%s': %s" % (box_path, str(res_box_access)))
