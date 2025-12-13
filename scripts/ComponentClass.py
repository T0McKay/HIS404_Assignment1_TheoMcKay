from LocationClass import Location
from enum import Enum

class StatusT(Enum):
    MANUFACTURING = 0
    AIRCRAFT = 1
    STORAGE = 2
    SCRAPPED = 3
    UNKNOWN = 4

class Component:
    def __init__(self, componentID : int, componentType : str, quantity : int, status : StatusT, location : Location):
        self.componentID = componentID
        self.componentType = componentType
        self.quantity = quantity
        self.status = status
        self.location = location

