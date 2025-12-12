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
    def __init__(self, locationID,name, locationType, postcode):
        self.locationID = locationID
        self.name = name
        self.type = locationType
        self.postcode = postcode

