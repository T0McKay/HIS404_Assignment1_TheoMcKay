from LocationClass import Location
from enum import Enum

#-----------------------------------------------------------------------------------------
# StatusT is an enumeration that stores the different statuses that a component can be in
#-----------------------------------------------------------------------------------------

class StatusT(Enum):
    MANUFACTURING = 0
    AIRCRAFT = 1
    STORAGE = 2
    SCRAPPED = 3
    UNKNOWN = 4

#----------------------------------------------------------------------------------------
# Component class defines a template for component objects.
# These are the objects being tracked within this system and feature in maintenance logs
#----------------------------------------------------------------------------------------

class Component:
    def __init__(self, componentID : int, componentType : str, quantity : int, status : StatusT, location : Location):
        self.componentID = componentID
        self.componentType = componentType
        self.quantity = quantity
        self.status = status
        self.location = location

    def getComponentID(self) :
        return self.componentID
    
    def getComponentType(self) :
        return self.componentType
    
    def getQuantity(self) :
        return self.quantity
    
    def getStatus(self) :
        return self.status
    
    def getLocation(self) :
        return self.location
    
    def updateComponent(self, compType, quantity, status, location) :
        self.componentType = compType
        self.quantity = quantity
        self.status = status
        self.location = location