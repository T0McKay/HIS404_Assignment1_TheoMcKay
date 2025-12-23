from UIManagerClass import UIManager
from DatabaseManagerClass import DatabaseManager

class System :

    @classmethod
    def systemStartup(cls) :
        DatabaseManager.initialLoad()
        UIManager.displayLoginPage()