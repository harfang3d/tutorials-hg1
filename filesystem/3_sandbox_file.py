# Sand-boxed access to the file system

import os
import harfang as hg

# mount two std file driver under two different prefixes, only one acts as a sandbox
hg.MountFileDriver(hg.StdFileDriver(os.path.dirname(__file__)), "std:")
hg.MountFileDriver(hg.StdFileDriver(os.path.dirname(__file__), True), "box:")

# access the readme.txt file outside of the std file driver root directory:
std_path = "std:../_data/owl.jpg"
res_std_access = hg.GetFilesystem().Exists(std_path)

# do the same on the sandboxed box: mount point
box_path = "box:../_data/owl.jpg"
res_box_access = hg.GetFilesystem().Exists(box_path)

print("Can access '%s' (expect OK): %s" % (std_path, str(res_std_access)))
print("Can access '%s' (expect KO): %s" % (box_path, str(res_box_access)))
