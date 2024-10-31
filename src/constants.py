from enum import Enum, auto

class StorageType(Enum):
    PICKLE = auto(),
    JSON = auto(),
    SQLITE = auto()