import sys
from hdf5helper import *

db_path = sys.argv[0]
folder_path = sys.argv[1]
save_path = sys.argv[2]

f = FileHelper(db_path)

f.store_from_folder(folder_path, save_path)

print('DONE')
