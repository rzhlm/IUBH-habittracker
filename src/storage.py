from constants import StorageType

class StorageStrategy:
    def add_habit(self, habit):
        pass
    def load_all(self):
        pass
    def save_all(self):
        pass

class StorageFactory:
    def create_storage(storage_type, save_file):
        match storage_type:
            case StorageType.PICKLE:
                return PickleStorage(save_file)
            case StorageType.JSON:
                return JSONStorage(save_file)
            case StorageType.SQLITE:
                return SQLiteStorage(save_file)
            case _:
                raise Exception("StorageFactory: no storage type given!")

class JSONStorage(StorageStrategy):
    pass
    
class PickleStorage(StorageStrategy):
    def __init__(self, savefile):
        self.savefile = savefile

    def load_all(self):
        pass

    def save_all(self):
        pass
    
class SQLiteStorage(StorageStrategy):
    pass