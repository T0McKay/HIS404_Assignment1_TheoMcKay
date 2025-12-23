import sqlite3
from EngineerClass import Engineer
from LocationClass import Location
from MaintenanceLogClass import MaintenanceLog
from ComponentClass import Component

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

#   -------------------------------------------------------------------------
#   ---                       Add Objects Method                          ---
#   --- Takes object, inserts using SQL, commits addition and disconnects ---
#   -------------------------------------------------------------------------

    @classmethod
    def addUserToDatabase(cls, object : Engineer) :
        #connecting to sqlite database
        conn = DatabaseManager.connect()
        #cursor object
        cursor = conn.cursor()

        role = ""
        if object.getIsManager :
            role += "MANAGER"
        else :
            role += "ENGINEER"

        #adds information to database for backup
        cursor.execute("""
            INSERT INTO Users (UserID, Name, Role, HashedPassword)
            VALUES (?, ?, ?, ?)
        """, (object.getUserID(), object.getName(), role, object.getHashedPassword()))

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
        """, (object.getLocationID(), object.getName(), object.getLocationType().name, object.getPostcode()))

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
            VALUES (?, ?, ?, ?, ?)
        """, (object.getLogID(), object.getDatePerformed(), object.getAction(), object.getComponent().getComponentID(), object.getUserPerforming().getUserID()))

        #commits and closes connection
        conn.commit()
        conn.close()

#   -------------------------------------------------------------------
#   ---                   Update Objects Method                     ---
#   --- Takes object, updates DB using SQL, commits and disconnects ---
#   -------------------------------------------------------------------

    @classmethod
    def updateComponentInDatabase(cls, component : Component) :
    #connecting to sqlite database
        conn = DatabaseManager.connect()
        #cursor object
        cursor = conn.cursor()

        #adds information to database for backup
        cursor.execute("""
            UPDATE Components
            SET Type = ?, Quantity = ?, Status = ?, LocationID = ?
            WHERE ComponentID = ?
        """, (component.getComponentType(), component.getQuantity(), component.getStatus().name, component.getLocation().getLocationID(), component.getComponentID()))

        #commits and closes connection
        conn.commit()
        conn.close()
