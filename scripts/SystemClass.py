from UIManagerClass import UIManager
from EngineerClass import Engineer

class System :
    loggedIn = False
    loggedInAs : Engineer

    @classmethod
    def getLoggedIn(cls) :
        return cls.loggedIn
    
    @classmethod
    def setLoggedIn(cls, isLoggedIn) :
        cls.loggedIn = isLoggedIn

    def getLoggedInAs(cls) :
        return cls.loggedInAs
    
    @classmethod
    def setLoggedInAs(cls, userLoggedIn : Engineer) :
        cls.loggedInAs = userLoggedIn

    @classmethod
    def systemStartup(cls) :
        UIManager.displayLoginPage()