from EngineerClass import Engineer
from ComponentClass import Component

#-----------------------------------------------------------------------------------
# Maintenance log is a class for log objects to be created.
# It stores the actions performed as well as the user and component objects related
#-----------------------------------------------------------------------------------

class MaintenanceLog:
    def __init__(self, logID : int, datePerformed : str, action : str, component : Component, userPerforming : Engineer):
        self.logID = logID
        self.datePerformed = datePerformed
        self.action = action
        self.component = component
        self.userPerforming = userPerforming

    def getLogID(self) :
        return self.logID
    
    def getDatePerformed(self) :
        return self.datePerformed
    
    def getAction(self) :
        return self.action
    
    def getComponent(self) :
        return self.component
    
    def getUserPerforming(self) :
        return self.userPerforming

