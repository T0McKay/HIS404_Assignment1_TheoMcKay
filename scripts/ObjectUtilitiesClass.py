import bcrypt
from datetime import datetime
from EngineerClass import Engineer
from MaintenanceLogClass import MaintenanceLog
from ComponentClass import Component
from DatabaseManagerClass import DatabaseManager

#---------------------------------------------------------------------------------
# The Object Tracker class is intended to be keep track of loaded objects
# Objects include locations, engineers, managers, components and maintenance logs
#---------------------------------------------------------------------------------

class ObjectUtilities :
    locations = []
    components = []
    maintenanceLogs = []
    users = []

    loggedIn = False
    loggedInAs : Engineer

#   ----------------------------------------------------------------------
#   ---                   User Logged In Management                    ---
#   --- Getters and setters for log in status and user if there is one ---
#   ----------------------------------------------------------------------

    @classmethod
    def getLoggedIn(cls) :
        return cls.loggedIn
    
    @classmethod
    def setLoggedIn(cls, isLoggedIn) :
        cls.loggedIn = isLoggedIn

    @classmethod
    def getLoggedInAs(cls) :
        return cls.loggedInAs
    
    @classmethod
    def setLoggedInAs(cls, userLoggedIn : Engineer) :
        cls.loggedInAs = userLoggedIn


#   -----------------------------------------------------
#   ---             Location Management               ---
#   --- Getters (for a location AND num of) + setters ---
#   -----------------------------------------------------

    @classmethod
    def addLocation(cls, location) :
        cls.locations.append(location)

    @classmethod
    def getNumLocations(cls) : 
        return len(cls.locations)
    
    @classmethod
    def getLocation(cls, index) :
        return cls.locations[index]

#   ------------------------------------------------------
#   ---              Component Management              ---
#   --- Getters (for a component AND num of) + setters ---
#   ------------------------------------------------------

    @classmethod
    def addComponent(cls, comp) :
        cls.components.append(comp)

    @classmethod
    def getNumComponents(cls) :
        return len(cls.components)
    
    @classmethod
    def getComponent(cls, index) :
        return cls.components[index]

    @classmethod
    def successfulComponentUpdate(cls, compID, compType, quantity, status, location) :
        for comp in range(ObjectUtilities.getNumComponents()) :
            component : Component = ObjectUtilities.getComponent(comp)
            if component.getComponentID() == int(compID) :
                
                #add operational log to compare and record changes?
                operationalLogMessage = ""

                if component.getComponentType() != compType :
                    operationalLogMessage += "Type changed. "
                
                if component.getQuantity() > quantity :
                    operationalLogMessage += "Quantity decreased. "
                elif component.getQuantity() < quantity :
                    operationalLogMessage += "Quantity increased. "

                if component.getStatus() != status :
                    operationalLogMessage += "Status changed. "

                if component.getLocation() != location :
                    operationalLogMessage += "Location changed."

                if operationalLogMessage != "" : #meaning no changes have been made
                    component.updateComponent(compType=compType, quantity=quantity, status=status, location=location)

                    ObjectUtilities.createAutomatedOperationalLog(operationalLogMessage, component=component)

                    #returns true to say it has updated component successfully
                    return component
                
        #if exits for loop then either component attributes never changed or component was not found so needs to return false
        return None

#   -------------------------------------------------
#   ---             User Management               ---
#   --- Getters (for a user AND num of) + setters ---
#   -------------------------------------------------

    @classmethod
    def addUser(cls, user) :
        cls.users.append(user)
    
    @classmethod
    def getNumUsers(cls) :
        return len(ObjectUtilities.users)
    
    @classmethod
    def getUser(cls, index) :
        return ObjectUtilities.users[index]

#   ------------------------------------------------
#   ---        Maintenance Log Management        ---
#   --- Getters (for a log AND num of) + setters ---
#   ------------------------------------------------

    @classmethod
    def addMaintenanceLog(cls, log) :
        cls.maintenanceLogs.append(log)

    @classmethod
    def getNumLogs(cls) :
        return len(cls.maintenanceLogs)
    
    @classmethod
    def getLog(cls, index) :
        return cls.maintenanceLogs[index]
    
    @classmethod
    def getNextLogID(cls) :
        return cls.maintenanceLogs[ObjectUtilities.getNumLogs() -1].getLogID() + 1

    @classmethod
    def createAutomatedOperationalLog(cls, actionCompleted, component) :
        todaysDate = datetime.today().strftime("%d/%m/%Y")
        newLog = MaintenanceLog(logID=ObjectUtilities.getNextLogID(), datePerformed=todaysDate, action=actionCompleted, component=component, userPerforming=ObjectUtilities.getLoggedInAs())
        ObjectUtilities.addMaintenanceLog(newLog)
        DatabaseManager.addLogToDatabase(newLog)

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
                    ObjectUtilities.loggedInAs = user 
                    ObjectUtilities.loggedIn = True
                    return True
            #exits for loop so return false as user not found
            return False
        except ValueError :
            return False
        