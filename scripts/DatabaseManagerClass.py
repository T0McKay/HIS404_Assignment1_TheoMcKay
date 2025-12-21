import sqlite3
from EngineerClass import Engineer
from ManagerClass import Manager
from LocationClass import Location
from MaintenanceLogClass import MaintenanceLog
from ComponentClass import Component, StatusT
from ObjectUtilitiesClass import ObjectUtilities

#-------------------------------------------------------------------------------------------------
# Database Manager class is used any time a connection, lookup and update is made to the database
# Acts as a static class using class methods and attributes. Cannot create objects of this class
#-------------------------------------------------------------------------------------------------

class DatabaseManager:

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
            ObjectUtilities.addLocation(newLocation)


        #---------------------------------------------
        #--- Loads Component Objects from Database ---
        #---------------------------------------------
        
        cursor.execute("SELECT * FROM Components")
        output = cursor.fetchall()

        for row in output:  
            #gets status and converts to statusT enum
            compStatus = row["Status"]
            status = StatusT[compStatus]

            #gets location object of component
            for location in ObjectUtilities.locations:
                if row["LocationID"] == location.getLocationID() : 
                    compLocation = location

            newComp = Component(componentID=row["ComponentID"], componentType=row["Type"], quantity=row["Quantity"], status=status, location=compLocation)
            ObjectUtilities.addComponent(newComp)

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

            ObjectUtilities.addUser(newUser)

        #---------------------------------------------------
        #--- Loads Maintenance Log Objects from Database ---
        #---------------------------------------------------
        
        cursor.execute("SELECT * FROM MaintenanceLogs")
        output = cursor.fetchall()

        for row in output:
            #gets component object of maintenance log
            for component in ObjectUtilities.components:
                if row["ComponentID"] == component.getComponentID() : 
                    logComp = component

            #gets user object of maintenance log
            for user in ObjectUtilities.users:
                if row["UserID"] == user.getUserID() : 
                    logUser = user

            newLog = MaintenanceLog(logID=row["LogID"], datePerformed=row["DatePerformed"], action=row["Action"], component=logComp, userPerforming=logUser)
            ObjectUtilities.addMaintenanceLog(newLog)

        #connection closed as no longer needed
        conn.close()

#   -------------------------------------------------------------------------
#   ---                       Add Objects Method                          ---
#   --- Takes object, inserts using SWL, commits addition and disconnects ---
#   -------------------------------------------------------------------------

    @classmethod
    def addUserToDatabase(cls, object : Engineer) :
        #connecting to sqlite database
        conn = DatabaseManager.connect()
        #cursor object
        cursor = conn.cursor()

        #adds information to database for backup
        cursor.execute("""
            INSERT INTO Users (UserID, Name, Role, HashedPassword)
            VALUES (?, ?, ?, ?)
        """, (object.getUserID(), object.getName(), "ENGINEER", object.getHashedPassword())) #will be updated in future to implement roles

        #commits and closes connection
        conn.commit()
        conn.close()

    @classmethod
    def addLocationToDatabase(cls, object : Location) :
        #connecting to sqlite database
        conn = DatabaseManager.connect()
        #cursor object
        cursor = conn.cursor()

        #adds information to database for backup
        cursor.execute("""
            INSERT INTO Locations (LocationID, Name, Type, Postcode)
            VALUES (?, ?, ?, ?)
        """, (object.getLocationID(), object.getName(), object.getLocationType(), object.getPostcode()))

        #commits and closes connection
        conn.commit()
        conn.close()

    @classmethod
    def addComponentToDatabase(cls, object : Component) :
        #connecting to sqlite database
        conn = DatabaseManager.connect()
        #cursor object
        cursor = conn.cursor()

        #adds information to database for backup
        cursor.execute("""
            INSERT INTO Components (ComponentID, Type, Quantity, Status, LocationID)
            VALUES (?, ?, ?, ?, ?)
        """, (object.getComponentID(), object.getComponentType(), object.getQuantity(), object.getStatus().name, object.getLocation().getLocationID()))

        #commits and closes connection
        conn.commit()
        conn.close()

    @classmethod
    def addLogToDatabase(cls, object : MaintenanceLog) :
        #connecting to sqlite database
        conn = DatabaseManager.connect()
        #cursor object
        cursor = conn.cursor()

        #adds information to database for backup
        cursor.execute("""
            INSERT INTO MaintenanceLogs (LogID, DatePerformed, Action, ComponentID, UserID)
            VALUES (?, ?, ?, ?)
        """, (object.getLogID(), object.getDatePerformed(), object.getAction(), object.getComponent().getComponentID(), object.getUserPerforming().getUserID()))

        #commits and closes connection
        conn.commit()
        conn.close()