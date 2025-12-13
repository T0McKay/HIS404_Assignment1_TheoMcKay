from EngineerClass import Engineer
from ComponentClass import Component

class MaintenanceLog:
    def __init__(self, logID : int, datePerformed : str, action : str, relatedComponent : Component, userPerforming : Engineer):
        self.logID = logID
        self.datePerformed = datePerformed
        self.action = action
        self.relatedComponent = relatedComponent
        self.userPerforming = userPerforming

