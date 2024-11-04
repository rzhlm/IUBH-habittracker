from constants import StorageType
import json

class StorageStrategy:
    def add_habit(self):
        pass
    def load_all(self):
        pass
    def save_all(self):
        pass

class StorageFactory:
    unique = False
    """     
    def __call__(cls, storage_type, save_file):
    if cls not in cls.unique:
        cls.unique[cls] = super(cls).__call__(storage_type,save_file)
    return cls.unique[cls]
    """
    
    def create_storage(cls, storage_type, save_file):
        
            match storage_type:
                case StorageType.PICKLE:
                    st = PickleStorage(save_file)
                    return st
                case StorageType.JSON:
                    st = JSONStorage(save_file)
                    return st
                case StorageType.SQLITE:
                    st = SQLiteStorage(save_file)
                    return st
                case _:
                    raise Exception("StorageFactory: no storage type given!")
            return cls.unique[cls]

class JSONStorage(StorageStrategy):
    def __init__(self, savefile):
        self.savefile = savefile
    
    def load_all(self):
        pass

    def save_all(self):
        pass
    
class PickleStorage(StorageStrategy):
    def __init__(self, savefile):
        self.savefile = savefile

    def load_all(self):
        pass

    def save_all(self):
        pass
    
class SQLiteStorage(StorageStrategy):
    def __init__(self, savefile):
        pass

    def load_all(self):
        pass

    def save_all(self):
        pass