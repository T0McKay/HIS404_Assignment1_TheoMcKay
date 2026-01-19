from NotificationClass import Notification
from ObjectUtilitiesClass import ObjectUtilities

#   --------------------------------------------------------------------------
#   ---                   Notification Manager Class                       ---
#   --- Used to manager notifications including updating, add and deleting ---
#   --------------------------------------------------------------------------

class NotificationManager :
    notifications : list[Notification] = []

#   --------------------------------------------------------------------
#   ---                   Update Notifications method                ---
#   --- Checks whole database and creates notifications of low stock ---
#   --------------------------------------------------------------------
    @classmethod
    def updateNotifications(cls) :
        cls.deleteNotifs()
        #then create notifs by checking each component
        for comp in range (ObjectUtilities.getNumComponents()) :
            queriedComponent = ObjectUtilities.getComponent(comp)
            
            newMessage = ""
            if queriedComponent.getQuantity() == 0 :
                newMessage = "IMMEDIATE RESTOCK REQUIRED. Component quantity is 0."
            elif queriedComponent.getQuantity() < 5 :
                newMessage = "RESTOCK RECOMMENDED. Component quantity low."  
                
            if newMessage != "" : 
                newNotif = Notification(notifID=comp, relatedComponent=queriedComponent, message=newMessage)
                cls.notifications.append(newNotif)

#   --------------------------------------------------------------
#   ---                Getter and Delete methods               ---
#   --- Used to get, get the number of or delete notifications ---
#   --------------------------------------------------------------
    @classmethod
    def deleteNotifs(cls) :
        for notif in range(cls.getNumNotifs()) :
            notification = cls.getNotification(notif)
            #deletes old notifications to be updated saving memory space
            del notification
            del cls.notifications[notif]

    @classmethod
    def getNotification(cls, index) :
        return cls.notifications[index]

    @classmethod
    def getNumNotifs(cls) :
        return len(cls.notifications)