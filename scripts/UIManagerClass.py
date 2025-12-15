from tkinter import *
from tkinter import messagebox, ttk
from functools import partial
from ObjectUtilitiesClass import ObjectUtilities

class UIManager : 

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
        succeededUserLogin = ObjectUtilities.authenticateUser(userIDEntry, passwordEntry)
        
        if succeededUserLogin == False : 
            messagebox.showerror("Login Failed", "Invalid user ID or password.")
        else :
            UIManager.windowNavigator()

    @classmethod
    def windowNavigator(cls) :
        #once login is correct then opens new database window
        UIManager.inventoryWindow()
        #in database there is a menu with : components, add component, maintenance logs, add log

    @classmethod
    def inventoryWindow(cls) :
        #gets route window with standardised title and menu bar
        root = UIManager.createWindow()

        #component table created with column headers
        treeView = ttk.Treeview(root, columns=("ComponentID", "Type", "Quantity", "Status", "Location"), show="headings")

        #prints headers
        for col in ("ComponentID", "Type", "Quantity", "Status", "Location") :
            treeView.heading(col, text=col)
            treeView.column(col, anchor="center", stretch=True, width=100)

        #displays loaded components in table
        for component in range(ObjectUtilities.getNumComponents()) :
            comp = ObjectUtilities.getComponent(component)
            treeView.insert("", "end", values=(str(comp.getComponentID()), str(comp.getComponentType()), str(comp.getQuantity()), str(comp.getStatus()), comp.getLocation().getName()))

        treeView.pack(padx=5, pady=5, expand=True)
        root.mainloop()



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
