from NotificationClass import Notification
from ObjectUtilitiesClass import ObjectUtilities

class NotificationManager :
    #needs to be a static class so uses class methods

    #stores array
    notifications : list[Notification] = []

    #needs a constant checker to be called every time page is opened/button refresh
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