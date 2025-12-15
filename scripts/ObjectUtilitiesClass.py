import bcrypt

#---------------------------------------------------------------------------------
# The Object Tracker class is intended to be keep track of loaded objects
# Objects include locations, engineers, managers, components and maintenance logs
#---------------------------------------------------------------------------------

class ObjectUtilities :
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

#   ----------------------------------------------------------
#   ---                Hash String Method                  ---
#   --- Converts string to bytes, generates a salt to hash ---
#   ---           Will be used to hash passwords           ---
#   ----------------------------------------------------------
    @classmethod
    def hashString(cls, rawString) :
        #converts string to bytes, creates a salt and hashes string
        byteString = rawString.encode('utf-8')
        salt = bcrypt.gensalt()
        hashedString = bcrypt.hashpw(byteString, salt)
        return hashedString