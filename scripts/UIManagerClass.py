from tkinter import *
from tkinter import messagebox
from functools import partial
from ObjectUtilitiesClass import ObjectUtilities

class UIManager : 

    @classmethod
    def displayWindows(cls) :
        #start with login page
        UIManager.displayLoginPage()

        #once login is correct then opens new database window

        #in database there is a menu with : components, add component, maintenance logs, add log


    @classmethod
    def displayLoginPage(cls) :
        # creates a root window
        root = Tk()
        root.title("WSG Login")
        root.geometry('700x400')
        root.resizable(False, False)

        #creates container for login form:
        frame = Frame(root)
        frame.pack(expand=True)

        #userID label and input box
        userIDLabel = Label(frame, text="User ID:")
        userIDLabel.pack(pady=5)
        userID = StringVar()
        userIDEntry = Entry(frame, textvariable=userID)
        userIDEntry.pack(pady=5)

        #password label and input box
        passwordLabel = Label(frame,text="Password:")
        passwordLabel.pack(pady=5) 
        password = StringVar()
        passwordEntry = Entry(frame, textvariable=password, show='*') #asterisks covers password while writing
        passwordEntry.pack(pady=5)

        #partial function created to pass parameters when button is clicked
        attemptLoginPartialFunc = partial(UIManager.authenticateLogin, usr=userID, pwd=password)

        #login button
        loginButton = Button(frame, text="Login", command=attemptLoginPartialFunc)
        loginButton.pack(pady=5)

        # Start the Tkinter event loop
        root.mainloop()

    @classmethod
    def authenticateLogin(cls, usr, pwd) :
        # user ID and password entrys must only be gotten when button is clicked, otherwise it will be null
        userIDEntry = usr.get()
        passwordEntry = pwd.get()
        
        #calls authenticate method which returns bool 
        succeededLogin = ObjectUtilities.authenticateUser(userIDEntry, passwordEntry)
        #if bool true then swap page
        if succeededLogin : 
            #open new inventory window
            messagebox.showerror("Success!", "It works!")
        else :
            #show error
            messagebox.showerror("Login Failed", "Invalid user ID or password.")


    @classmethod
    def createWindow(cls) :
        # creates a root window
        root = Tk()

        #root window title and dimensions (width x height)
        root.title("WSG Inventory Tool")
        root.geometry('700x400')
        root.resizable(False, False)

        menu = Menu(root)
        root.config(menu=menu)

        inventoryMenu = Menu(menu, tearoff=0)
        inventoryMenu.add_command(label="View") # NEED TO ADD COMMAND
        inventoryMenu.add_command(label="Add Component") # NEED TO ADD COMMAND
        inventoryMenu.add_command(label="Add Log Entry") # NEED TO ADD COMMAND

        menu.add_cascade(label="Inventory", menu=inventoryMenu)

        menu.add_cascade(label="Notifications", command=root.destroy) # NEED TO ADD COMMAND
        menu.add_cascade(label="Log Out", command=root.destroy)

        return root

    @classmethod
    def swapWindows(cls, oldWindow, newWindow) :
        pass
