#will have to import engineer and component classes

class MaintenanceLog:
    def __init__(self, logID, datePerformed, action, relatedComponent, userPerforming):
        self.logID = logID
        self.datePerformed = datePerformed
        self.action = action
        self.relatedComponent = relatedComponent
        self.userPerforming = userPerforming

