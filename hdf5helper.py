import numpy as np
import h5py
import os


class FileHelper(object):

    def __init__(self, db):
        self.db = h5py.File(db)

    def get(self):
        return self.db

    def get(self, path):
        return self.db[path]

    def list(self, path):
        return [key for key in self.db[path].keys()]

    def list_attr(self, path):
        return [key for key in self.db[path].attrs.keys()]

    def store_file(self, path, store_path):
        file = open(path, 'rb')
        try:
            dt = h5py.special_dtype(vlen=np.dtype('uint8'))
            temp = self.db.create_dataset(store_path, (1,), dtype=dt)
        except:
            temp = self.db[store_path]

        temp[0] = np.fromstring(file.read(), dtype='uint8')

    def store_from_folder(self, path, save_path=""):
        directory = os.fsencode(path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            self.store_file(path + filename, save_path + filename)