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
    pass
    
class SQLiteStorage(StorageStrategy):
    pass