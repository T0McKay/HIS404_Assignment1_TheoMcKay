#---------------------------------------------------------------------------------
# The Object Tracker class is intended to be keep track of loaded objects
# Objects include locations, engineers, managers, components and maintenance logs
#---------------------------------------------------------------------------------

class ObjectTracker :
    locations = []
    components = []
    users = []
    maintenanceLogs = []

    def addLocation(cls, location) :
        cls.locations.append[location]
    
    def addComponent(cls, comp) :
        cls.components.append[comp]
    
    def addUser(cls, user) :
        cls.users.append[user]
    
    def addMaintenanceLog(cls, log) :
        cls.maintenanceLogs.append[log]