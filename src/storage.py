class StorageStrategy:
    def add_habit(self, habit):
        pass
    def load_all(self):
        pass
    def save_all(self):
        pass

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