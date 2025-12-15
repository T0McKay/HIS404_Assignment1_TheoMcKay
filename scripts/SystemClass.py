from UIManagerClass import UIManager

class System :
    loggedIn = False

    @classmethod
    def getLoggedIn(cls) :
        return cls.loggedIn
    
    @classmethod
    def setLoggedIn(cls, isLoggedIn) :
        cls.loggedIn = isLoggedIn

    @classmethod
    def systemStartup(cls) :
        UIManager.displayWindows()