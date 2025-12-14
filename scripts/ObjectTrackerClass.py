

#---------------------------------------------------------------------------------
# The Object Tracker class is intended to be keep track of loaded objects
# Objects include locations, engineers, managers, components and maintenance logs
#---------------------------------------------------------------------------------

class ObjectTracker :
    locations = []
    components = []
    users = []
    maintenanceLogs = []

    @classmethod
    def addLocation(cls, location) :
        cls.locations.append(location)
    
    @classmethod
    def addComponent(cls, comp) :
        cls.components.append(comp)
    
    @classmethod
    def addUser(cls, user) :
        cls.users.append(user)
    
    @classmethod
    def addMaintenanceLog(cls, log) :
        cls.maintenanceLogs.append(log)