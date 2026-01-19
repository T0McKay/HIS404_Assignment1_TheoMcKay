from UIManagerClass import UIManager
from DatabaseManagerClass import DatabaseManager
from ObjectUtilitiesClass import ObjectUtilities
from LocationClass import Location, LocationT
from ComponentClass import Component, StatusT
from EngineerClass import Engineer
from MaintenanceLogClass import MaintenanceLog

class System :

    @classmethod
    def systemStartup(cls) :
        System.initialLoad()
        UIManager.displayLoginPage()

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
            #gets type and converts to LocationT enum
            locType = row["Type"]
            locationType = LocationT[locType]

            #row is an sqliteRow so can access using column names
            newLocation = Location(locationID=row["LocationID"], name=row["Name"], locationType=locationType, postcode=row["Postcode"])
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
                newUser = Engineer(userID=row["UserID"], name=row["Name"], hashedPassword=row["HashedPassword"], isManager=True)
            else : #engineer role
                newUser = Engineer(userID=row["UserID"], name=row["Name"], hashedPassword=row["HashedPassword"], isManager=False)

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

System.systemStartup()