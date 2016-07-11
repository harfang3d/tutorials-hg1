# Access to the file system

import os
import gs

# mount the system file driver, StdFileDriver wraps the system native file API
gs.MountFileDriver(gs.StdFileDriver())

# test that we indeed have access to the file system
path = os.path.realpath(__file__)  # absolute path to this file on the file system
result = gs.GetFilesystem().Exists(path)  # can the engine file system see it?

print("Access OK: %s" % str(result))
