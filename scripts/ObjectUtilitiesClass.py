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

    @classmethod
    def getNumComponents(cls) :
        return len(cls.components)
    
    @classmethod
    def getComponent(cls, index) :
        return cls.components[index]

#   ----------------------------------------------------------
#   ---                Hash String Method                  ---
#   --- Converts string to bytes, generates a salt to hash ---
#   ---           Will be used to hash passwords           ---
#   ----------------------------------------------------------
    @classmethod
    def hashString(cls, rawString) :
        byteString = rawString.encode('utf-8')
        salt = bcrypt.gensalt()
        hashedString = bcrypt.hashpw(byteString, salt).strip().decode() #.decode gets rid of python wrapper for byte objects
        return hashedString
    
#   ---------------------------------------------------------------------------
#   ---                     Authenticate User Method                        ---
#   --- Compares entered userIDs and passwords. Returns true if user exists ---
#   ---------------------------------------------------------------------------
    @classmethod
    def authenticateUser(cls, checkUserID, checkPassword) :
        # tries to convert entered userID to int, if it doesn't work then its incorrect
        try :
            checkUserID = int (checkUserID)
            for user in ObjectUtilities.users :
                if checkUserID == user.userID and bcrypt.checkpw(checkPassword.encode('utf-8'), user.hashedPassword.encode('utf-8')) : 
                    return True
                else :
                    return False
        except ValueError :
            return False
        