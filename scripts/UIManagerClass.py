from tkinter import *
from tkinter import messagebox, ttk
from functools import partial
from ObjectUtilitiesClass import ObjectUtilities
from ComponentClass import StatusT, Component
from DatabaseManagerClass import DatabaseManager

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
        attemptLoginPartialFunc = partial(UIManager.authenticateLogin, usr=userID, pwd=password, rootWindow=root)

        #login button
        loginButton = Button(frame, text="Login", command=attemptLoginPartialFunc)
        loginButton.pack(pady=5)

        # Start the Tkinter event loop
        root.mainloop()

    @classmethod
    def authenticateLogin(cls, rootWindow : Tk, usr, pwd) :
        # user ID and password entrys must only be gotten when button is clicked, otherwise it will be null
        userIDEntry = usr.get()
        passwordEntry = pwd.get()
        
        #calls authenticate method which returns bool
        succeededUserLogin = ObjectUtilities.authenticateUser(userIDEntry, passwordEntry)
        
        if succeededUserLogin == False : 
            messagebox.showerror("Login Failed", "Invalid user ID or password.")
        else :
            rootWindow.destroy()
            UIManager.showInventoryPage()

    @classmethod
    def createWindowMenu(cls) :
        # creates a root window
        root = Tk()

        #root window title and dimensions (width x height)
        root.title("WSG Inventory Tool")
        root.geometry('700x400')
        root.resizable(False, False)

        menu = Menu(root)
        root.config(menu=menu)

        inventoryMenu = Menu(menu, tearoff=0)
        inventoryMenu.add_command(label="View Components", command=UIManager.showInventoryPage)
        inventoryMenu.add_cascade(label="View MaintenanceLogs", command=UIManager.showMaintenanceLogs)
        inventoryMenu.add_command(label="Add Component", command=UIManager.addComponentPage)
        inventoryMenu.add_command(label="Add Log Entry") # NEED TO ADD COMMAND

        menu.add_cascade(label="Inventory", menu=inventoryMenu)
        menu.add_cascade(label="Notifications", command=root.destroy) # NEED TO ADD COMMAND
        menu.add_cascade(label="Log Out", command=root.destroy)

        return root

    @classmethod
    def showInventoryPage(cls) :
        #gets route window with standardised title and menu bar
        root = UIManager.createWindowMenu()

        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #component table created with column headers
        treeView = ttk.Treeview(root, columns=("ComponentID", "Type", "Quantity", "Status", "Location"), show="headings")

        #prints headers
        for col in ("ComponentID", "Type", "Quantity", "Status", "Location") :
            treeView.heading(col, text=col)
            treeView.column(col, anchor="center", stretch=True, width=100)

        #displays loaded components in table
        for component in range(ObjectUtilities.getNumComponents()) :
            comp = ObjectUtilities.getComponent(component)
            treeView.insert("", "end", values=(str(comp.getComponentID()), str(comp.getComponentType()), str(comp.getQuantity()), comp.getStatus().name, comp.getLocation().getName()))

        #scrollbar 
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeView.yview)
        treeView.configure(yscrollcommand=scrollbar.set)

        treeView.pack(padx=5, pady=5, expand=True)
        root.mainloop()

    @classmethod
    def showMaintenanceLogs(cls) : 
        #gets route window with standardised title and menu bar
        root = UIManager.createWindowMenu()

        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #component table created with column headers
        treeView = ttk.Treeview(root, columns=("LogID", "Component", "Action", "Date", "User"), show="headings")

        #prints headers
        for col in ("LogID", "Component", "Action", "Date", "User") :
            treeView.heading(col, text=col)
            treeView.column(col, anchor="center", stretch=True, width=100)

        #displays loaded components in table
        for maintenanceLog in range(ObjectUtilities.getNumLogs()) :
            log = ObjectUtilities.getLog(maintenanceLog)
            treeView.insert("", "end", values=(str(log.getLogID()), str(log.getComponent().getComponentID()), str(log.getAction()), str(log.getDatePerformed()), log.getUserPerforming().getName()))

        #scrollbar 
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeView.yview)
        treeView.configure(yscrollcommand=scrollbar.set)

        treeView.pack(padx=5, pady=5, expand=True)
        root.mainloop()

    @classmethod
    def addComponentPage(cls) : 
        #creates popup to enter component details
        addCompPopup = Toplevel()
        addCompPopup.title("Add Component")
        addCompPopup.geometry("300x500")
        addCompPopup.resizable(False, False)

        #component ID label and input box
        compIDLabel = Label(addCompPopup, text="Component ID:")
        compIDLabel.pack(pady=5)
        compID = StringVar()
        compIDEntry = Entry(addCompPopup, textvariable=compID)
        compIDEntry.pack(pady=5)

        def verifyUniqueComponentID(userInput) :
            try :
                userInput = int(userInput)
                if userInput > 0 :
                    for comp in range(ObjectUtilities.getNumComponents()) :
                        if ObjectUtilities.getComponent(comp).getComponentID() == userInput :
                            return -1
                    #has exited for statement:
                    return userInput
                else :
                    return -1
            except Exception :
                return -1

        #component type label and input box
        compTypeLabel = Label(addCompPopup, text="Component Type:")
        compTypeLabel.pack(pady=5)
        compType = StringVar()
        compTypeEntry = Entry(addCompPopup, textvariable=compType)
        compTypeEntry.pack(pady=5)

        #quantity label and input box
        compQuantityLabel = Label(addCompPopup, text="Component Quantity:")
        compQuantityLabel.pack(pady=5)
        compQuantity = StringVar()
        compQuantityEntry = Entry(addCompPopup, textvariable=compQuantity)
        compQuantityEntry.pack(pady=5)

        #method to verify quantity:
        def verifyQuantity(userInput) :
            try :
                toReturn = int(userInput)
                if toReturn > 0 :
                    return toReturn
                else :
                    return -1
            except Exception :
                return -1

        #status label and input box / drop down
        compStatusLabel = Label(addCompPopup, text="Component Status:")
        compStatusLabel.pack(pady=5)
        statusNames = []
        for status in StatusT :
            statusNames.append(status.name)
        statusSelect = ttk.Combobox(addCompPopup, values=statusNames, state="readonly")
        statusSelect.pack()

        #location label and input box / drop down
        compLocationLabel = Label(addCompPopup, text="Component Location:")
        compLocationLabel.pack(pady=5)
        #pulls location names and ID from object utilities
        locations = {}
        for loc in range(ObjectUtilities.getNumLocations()) : 
            location = ObjectUtilities.getLocation(loc)
            locations[location.getName()] = location
        locationSelect = ttk.Combobox(addCompPopup, values=list(locations.keys()), state="readonly")
        locationSelect.pack()

        #embedded submit function to be executed on button click
        def submit() :
            validSubmission = True
            
            #gets component ID
            selectedComponentID = verifyUniqueComponentID(compIDEntry.get())
            if selectedComponentID == -1 :
                validSubmission = False

            #gets component type
            selectedComponentType = compTypeEntry.get()

            #gets quantity of components
            selectedQuantity = verifyQuantity(compQuantityEntry.get())
            if selectedQuantity == -1 :
                validSubmission = False
            
            #gets status from box
            selectedStatusName = statusSelect.get()
            try :
                selectedStatus = StatusT[selectedStatusName]
            except Exception :
                validSubmission = False

            #gets location from dropdown box
            selectedLocationName = locationSelect.get()
            try : 
                selectedLocation = locations[selectedLocationName]
            except Exception : 
                validSubmission = False

            if validSubmission == True : 
                #create component object
                newComponent = Component(componentID=selectedComponentID, componentType=selectedComponentType, quantity=selectedQuantity, status=selectedStatus, location=selectedLocation,)

                #update components array in object utilities
                ObjectUtilities.addComponent(newComponent)

                #write to database 
                DatabaseManager.addComponentToDatabase(newComponent)
                
                messagebox.showinfo("Success!", "Component has been added to inventory.")
                addCompPopup.destroy()
            else :
                messagebox.showerror("Invalid Component", "Please ensure ID is unique and quantities are positive integers.")

        #button to submit new component to be added
        submitComponentButton = ttk.Button(addCompPopup, text="Add Component", command=submit)
        submitComponentButton.pack(pady=15)
        
    @classmethod
    def showComponentViewPage(cls, root) : 
        #creates container for component search:
        frame = Frame(root)
        frame.pack(expand=True)

        #userID label and input box
        userIDLabel = Label(frame, text="User ID:")
        userIDLabel.pack(pady=5)
        userID = StringVar()
        userIDEntry = Entry(frame, textvariable=userID)
        userIDEntry.pack(pady=5)


