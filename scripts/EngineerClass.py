#--------------------------------------------------------------------------------------------------
# Engineer class is a template for objects storing information about users in the engineering role
# It is the superclass of the Manager class
#--------------------------------------------------------------------------------------------------

class Engineer:
    def __init__(self, userID : int, name : str, hashedPassword : str, isManager : bool):
        self.userID = userID
        self.name = name
        self.hashedPassword = hashedPassword
        self.isManager = isManager

    def getUserID(self) :
        return self.userID
    
    def getName(self) :
        return self.name
    
    def getHashedPassword(self) :
        return self.hashedPassword
    
    def getIsManager(self) :
        return self.isManager