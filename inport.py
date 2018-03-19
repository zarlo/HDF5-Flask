#!bin/python3
import sys
from hdf5helper import FileHelper

db_path = sys.argv[1]
folder_path = sys.argv[2]
save_path = sys.argv[3]

print(db_path)
print(folder_path)
print(save_path)

f = FileHelper(db_path)
print('i might add a ETA one day')
f.store_from_folder(folder_path, save_path, True)
print('DONE')
