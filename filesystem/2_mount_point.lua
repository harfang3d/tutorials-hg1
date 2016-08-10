-- Access to the file system through mount points

-- mount a standard file system as the 'std:' prefix
gs.MountFileDriver(gs.StdFileDriver(), "std:")

-- mount a standard file system pointing to the data directory as the 'data:' prefix
gs.MountFileDriver(gs.StdFileDriver('../_data'), 'data:')

-- name and relative path to a data file
file_name = 'owl.jpg'
file_path = '../_data/'..file_name

-- the engine can access the file by name through the 'data:' mount point
data_path = 'data:'..file_name
res_data_access = gs.GetFilesystem():Exists(data_path)

print("Can access '"..data_path.."': "..tostring(res_data_access))

-- and it can access it using its relative path through the std: mount point
std_path = 'std:'..file_path
res_std_access = gs.GetFilesystem():Exists(std_path)

print("Can access '"..std_path.."': "..tostring(res_std_access))
