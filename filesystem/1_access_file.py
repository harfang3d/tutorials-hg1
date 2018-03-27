# Access to the file system

import os
import harfang as hg

# mount the system file driver, StdFileDriver wraps the system native file API
hg.MountFileDriver(hg.StdFileDriver())

# test that we indeed have access to the file system
path = os.path.realpath(__file__)  # absolute path to this file on the file system
result = hg.GetFilesystem().Exists(path)  # can the engine file system see it?

print("Access OK: %s" % str(result))
