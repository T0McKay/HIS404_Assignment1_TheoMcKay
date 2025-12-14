from enum import Enum

class LocationT(Enum):
    WAREHOUSE = 1
    HANGAR = 2
    AIRCRAFT = 3
    WORKSHOP = 4
    LABORATORY = 5
    OFFICE = 6
    OTHER = 7

class Location:
    def __init__(self, locationID : int ,name : str, locationType : LocationT, postcode : str):
        self.locationID = locationID
        self.name = name
        self.locationType = locationType
        self.postcode = postcode

    def getLocationID(self) :
        return self.locationID
    
    def getName(self) :
        return self.name
    
    def getLocationType(self) :
        return self.locationType
    
    def getPostcode(self) :
        return self.postcode
