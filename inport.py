#!bin/python3
import sys
from hdf5helper import FileHelper
import tarfile

db_path = sys.argv[1]
folder_path = sys.argv[2]
save_path = sys.argv[3]

print(db_path)
print(folder_path)
print(save_path)


f = FileHelper(db_path)

if '.tar' in folder_path:
    tar = tarfile.open(folder_path)
    tar.getmember()
    for item in tar.getmembers():
        temp_file = tar.extractfile(item)
        file_data = temp_file.read()
        f.store_buff(file_data, item.name)
        file_data.close()
        
    tar.close()

else:
    print('i might add a ETA one day')
    f.store_from_folder(folder_path, save_path, True)
    print('DONE')
