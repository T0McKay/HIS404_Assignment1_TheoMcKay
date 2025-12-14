import sqlite3
from EngineerClass import Engineer
from ManagerClass import Manager
from LocationClass import Location
from MaintenanceLogClass import MaintenanceLog
from ComponentClass import Component

class DatabaseManager:
    #will act as static class but using static methods and class attributes - will also throw error if tries to instatiate
    locations = []
    components = []
    users = []
    maintenanceLogs = []

#   ---------------------------------------
#   ---        Connect method           ---
#   --- Establishes database connection ---
#   ---------------------------------------
    @classmethod
    def connect(cls):
        #Connects to database, or creates if it does not exist
        conn = sqlite3.connect("database.db")
        #allows columns to be accessed by name using dictionary-like row access
        conn.row_factory = sqlite3.Row 
        return conn

#   -----------------------------------------------------
#   ---            Initial Load Method                ---
#   --- Loads all Components and locations as objects ---
#   -----------------------------------------------------
    @classmethod
    def initialLoad(cls) :
        #connecting to sqlite database
        conn = DatabaseManager.connect()

        #cursor object
        cursor = conn.cursor()

        #--------------------------------------------
        #--- Loads Location Objects from Database ---
        #--------------------------------------------

        cursor.execute("SELECT * FROM Locations")
        output = cursor.fetchall()

        for row in output:
            #row is an sqliteRow so can access using column names
            newLocation = Location(locationID=row["LocationID"], name=row["Name"], locationType=row["Type"], postcode=row["Postcode"])
            DatabaseManager.locations.append(newLocation)


        #---------------------------------------------
        #--- Loads Component Objects from Database ---
        #---------------------------------------------
        
        cursor.execute("SELECT * FROM Components")
        output = cursor.fetchall()

        for row in output:
            #gets location object of component
            for location in DatabaseManager.locations:
                if row["LocationID"] == location.getLocationID() : 
                    compLocation = location

            newComp = Component(componentID=row["ComponentID"], componentType=row["Type"], quantity=row["Quantity"], status=row["Status"], location=compLocation)
            DatabaseManager.components.append(newComp)

        #----------------------------------------
        #--- Loads User Objects from Database ---
        #----------------------------------------

        cursor.execute("SELECT * FROM Users")
        output = cursor.fetchall()

        for row in output:
            if row["Role"] == "MANAGER" :
                newUser = Manager(userID=row["UserID"], name=row["Name"], hashedPassword=row["HashedPassword"])
            else : #engineer role
                newUser = Engineer(userID=row["UserID"], name=row["Name"], hashedPassword=row["HashedPassword"])

            DatabaseManager.users.append(newUser)

        #---------------------------------------------------
        #--- Loads Maintenance Log Objects from Database ---
        #---------------------------------------------------
        
        cursor.execute("SELECT * FROM MaintenanceLogs")
        output = cursor.fetchall()

        for row in output:
            #gets component object of maintenance log
            for component in DatabaseManager.components:
                if row["ComponentID"] == component.getComponentID() : 
                    logComp = component

            #gets user object of maintenance log
            for user in DatabaseManager.users:
                if row["UserID"] == user.getUserID() : 
                    logUser = user

            newLog = MaintenanceLog(logID=row["LogID"], datePerformed=row["DatePerformed"], action=row["Action"], component=logComp, userPerforming=logUser)
            DatabaseManager.maintenanceLogs.append(newLog)

        #connection closed as no longer needed
        conn.close()

    @classmethod
    def getRecord():
        
        pass

    #------------------------------------------------
    #----- POLYMORPHISM:                        -----
    #------------------------------------------------

    @classmethod
    def updateDatabase(object : Engineer) :
        pass

    @classmethod
    def updateDatabase(object : Location) :
        pass

    @classmethod
    def updateDatabase(object : Component) :
        pass

    @classmethod
    def updateDatabase(object : MaintenanceLog) :
        pass