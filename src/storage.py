from constants import StorageType
from abc import ABC, abstractmethod

"""
NOTE: This class is currently not used anywhere
It is unfinished, a placeholder.
"""

class StorageStrategy(ABC):
    """STORAGE: StorageStrategy"""
    @abstractmethod
    def add_habit(self):
        pass
    
    @abstractmethod
    def load_all(self):
        pass
    
    @abstractmethod
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
    
    def create_storage(self, save_file, storage_type = StorageType.JSON):
            """STORAGE: StorageFactory: creates a Storage object of
            the specified type"""
            
        
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
                    raise Exception("StorageFactory: no valid storage type given!")
            return cls.unique[cls]

class JSONStorage(StorageStrategy):
    """Storage: JSONStorage: creates a storage object,
    for use with JSON"""
    def __init__(self, savefile):
        self.savefile = savefile
    
    def load_all(self):
        pass

    def save_all(self):
        pass
    
class PickleStorage(StorageStrategy):
    """Storage: PickleStorage: creates a storage object,
    for use with Pickle"""
    def __init__(self, savefile):
        self.savefile = savefile

    def load_all(self):
        pass

    def save_all(self):
        pass
    
class SQLiteStorage(StorageStrategy):
    """Storage: SQLiteStorage: creates a storage object,
    for use with SQLite"""
    def __init__(self, savefile):
        pass

    def load_all(self):
        pass

    def save_all(self):
        pass