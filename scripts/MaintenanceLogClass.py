from EngineerClass import Engineer
from ComponentClass import Component

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

