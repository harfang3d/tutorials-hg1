# Access to the file system through mount points

import os
import harfang as hg

# mount a standard file system as the 'std:' prefix
hg.MountFileDriver(hg.StdFileDriver(), "std:")

# mount a standard file system pointing to the current directory as the 'cwd:' prefix
hg.MountFileDriver(hg.StdFileDriver(os.path.dirname(__file__)), "cwd:")

# get the full path to this file
this_file_path = os.path.realpath(__file__)

# get this file name (ie. path relative to the current directory)
this_file_name = os.path.basename(__file__)

# the engine can access it relative to the current directory through the 'cwd:' mount point
cwd_path = "cwd:" + this_file_name
res_cwd_access = hg.GetFilesystem().Exists(cwd_path)

# and it can access it using its absolute path through the std: mount point
std_path = "std:" + this_file_path
res_std_access = hg.GetFilesystem().Exists(std_path)

# however, when no prefix is specified the engine has no way to access it from its absolute path
res_direct_access = hg.GetFilesystem().Exists(this_file_path)

print("Can access '%s' (expect KO): %s" % (this_file_path, str(res_direct_access)))
print("Can access '%s' (expect OK): %s" % (cwd_path, str(res_cwd_access)))
print("Can access '%s' (expect OK): %s" % (std_path, str(res_std_access)))
