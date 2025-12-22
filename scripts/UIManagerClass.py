from tkinter import *
from tkinter import messagebox, ttk
from functools import partial
from ObjectUtilitiesClass import ObjectUtilities
from ComponentClass import StatusT, Component
from MaintenanceLogClass import MaintenanceLog
from DatabaseManagerClass import DatabaseManager

#   -----------------------------------------------------------------------------
#   ---                          UI Manager Class                             ---
#   --- Provides UI using tkinter library for user to interact with inventory ---
#   -----------------------------------------------------------------------------

class UIManager : 

#   --------------------------------------------------------------------------
#   ---                    Display Login Page Method                       ---
#   --- Provides label and text boxes for users to input IDs and passwords ---
#   --------------------------------------------------------------------------
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

#   ---------------------------------------------------------------------------
#   ---                     Authenticate Login Method                       ---
#   --- Used by login page to interact with Object utilities for validation ---
#   ---------------------------------------------------------------------------
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

#   -------------------------------------------------------------------------------------------
#   ---                                Create Window Menu                                   ---
#   --- Used by all page methods excluding login to create root with identical menu options ---
#   -------------------------------------------------------------------------------------------
    @classmethod
    def createWindowMenu(cls) :
        # creates a root window
        root = Tk()

        #root window title and dimensions (width x height)
        root.title("WSG Inventory Tool")
        root.geometry('700x300')
        root.resizable(False, False)

        menu = Menu(root)
        root.config(menu=menu)

        inventoryMenu = Menu(menu, tearoff=0)
        inventoryMenu.add_command(label="View Components", command=UIManager.showInventoryPage)
        inventoryMenu.add_cascade(label="View MaintenanceLogs", command=UIManager.showMaintenanceLogs)
        inventoryMenu.add_command(label="Add Component", command=UIManager.addComponentPage)
        inventoryMenu.add_command(label="Add Log Entry", command=UIManager.addLogPage) 

        menu.add_cascade(label="Inventory", menu=inventoryMenu)
        menu.add_cascade(label="Notifications", command=root.destroy) # NEED TO ADD COMMAND
        menu.add_cascade(label="Log Out", command=root.destroy)

        return root

#   ----------------------------------------------------------
#   ---                 Show Inventory Page                ---
#   --- Displays components currently loaded in at runtime ---
#   ----------------------------------------------------------
    @classmethod
    def showInventoryPage(cls) :
        #gets route window with standardised title and menu bar
        root = UIManager.createWindowMenu()

        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #inventory title label
        componentsLabel = Label(frame, text="Components Inventory")
        componentsLabel.pack(pady=5)

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

#   ----------------------------------------------------------------------------------------------
#   ---                               Show Maintenance Logs Page                               ---
#   --- Displays all maintenance logs independent of components currently loaded in at runtime ---
#   ----------------------------------------------------------------------------------------------
    @classmethod
    def showMaintenanceLogs(cls) : 
        #gets route window with standardised title and menu bar
        root = UIManager.createWindowMenu()

        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #maintenance logs title
        titleLabel = Label(frame, text="Maintenance Logs")
        titleLabel.pack(pady=5)

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

#   ------------------------------------------------------------------------------------------
#   ---                                  Add Component Page                                ---
#   --- Provides popup and authenticates new component, then requests addition to database ---
#   ------------------------------------------------------------------------------------------
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
        
#   ------------------------------------------------------------------------------------
#   ---                                  Add Log Page                                ---
#   --- Provides popup and authenticates new log, then requests addition to database ---
#   ------------------------------------------------------------------------------------
    @classmethod
    def addLogPage(cls) : 
        #creates popup to enter log details
        addLogPopup = Toplevel()
        addLogPopup.title("Add Operational Log")
        addLogPopup.geometry("300x400")
        addLogPopup.resizable(False, False)

        #log ID label and automated log ID
        logIDTitle = Label(addLogPopup, text="Log ID:")
        logIDTitle.pack(pady=5)
        logID = ObjectUtilities.getNextLogID()
        logIDLabel = Label(addLogPopup, text=str(logID))
        logIDLabel.pack(pady=5)

        #date performed label and input box - returns date as DD/MM/YYYY - need to add container for date

        #container to hold date labels and dropdowns
        dateContainer = Frame(addLogPopup)
        dateContainer.pack(pady=5)

        #creates container for labels
        dateLabelContainer = Frame(dateContainer)
        dateLabelContainer.pack(pady=5)

        #creates container for dropdowns
        dateSelectContainer = Frame(dateContainer)
        dateSelectContainer.pack(pady=5)

        dateLabel = Label(dateLabelContainer, text="Date Performed:")
        dateDayLabel = Label(dateLabelContainer, text="Day:")
        dateMonthLabel = Label(dateLabelContainer, text="Month:")
        dateYearLabel = Label(dateLabelContainer, text="Year:")

        #creates allowable days months and years and dropdown boxes
        days = list(range(1, 32))
        months = list(range(1, 13))
        years = list(range(2025, 2035))

        dayBox = ttk.Combobox(dateSelectContainer, values=days, width=5, state="readonly")
        monthBox = ttk.Combobox(dateSelectContainer, values=months, width=5, state="readonly")
        yearBox = ttk.Combobox(dateSelectContainer, values=years, width=7, state="readonly")

        #packs all labels, dropdowns and containers
        dateLabel.pack(pady=5)
        dateDayLabel.pack(side="left", padx=5)
        dateMonthLabel.pack(side="left", padx=5)
        dateYearLabel.pack(side="left", padx=5)
        dayBox.pack(side="left", padx=5)
        monthBox.pack(side="left", padx=5)
        yearBox.pack(side="left", padx=5)

        #action label and input box
        actionLabel = Label(addLogPopup, text="Action:")
        actionLabel.pack(pady=5)
        action = StringVar()
        actionEntry = Entry(addLogPopup, textvariable=action)
        actionEntry.pack(pady=5)

        #component label and input box / drop down
        compLabel = Label(addLogPopup, text="Component:")
        compLabel.pack(pady=5)
        components = {}
        for comp in range(ObjectUtilities.getNumComponents()) : 
            component = ObjectUtilities.getComponent(comp)
            components[component.getComponentID()] = component
        componentSelect = ttk.Combobox(addLogPopup, values=list(components.keys()), state="readonly")
        componentSelect.pack()

        #user performing action label and input box / drop down
        userLabel = Label(addLogPopup, text="User:")
        userLabel.pack(pady=5)
        #pulls location names and ID from object utilities
        users = {}
        for usr in range(ObjectUtilities.getNumUsers()) : 
            user = ObjectUtilities.getUser(usr)
            users[user.getName()] = user
        userSelect = ttk.Combobox(addLogPopup, values=list(users.keys()), state="readonly")
        userSelect.pack()

        #embedded submit function to be executed on button click
        def submit() :
            validSubmission = True

            #gets date using three day month and year drop downs
            try :
                selectedDay = dayBox.get()
            except Exception :
                validSubmission = False

            #gets month from box
            try :
                selectedMonth = monthBox.get()
            except Exception :
                validSubmission = False

            #gets year from box
            try :
                selectedYear = yearBox.get()
            except Exception :                    
                validSubmission = False

            #forms whole date
            selectedDatePerformed = str(selectedDay) + "/" + str(selectedMonth) + "/" + str(selectedYear)

            #gets action performed 
            enteredAction = actionEntry.get()
            
            #gets component from box
            selectedComponentID = int(componentSelect.get())
            try :
                selectedComp = components[selectedComponentID]
            except Exception :
                validSubmission = False

            #gets location from dropdown box
            selectedUserName = userSelect.get()
            try : 
                selectedUser = users[selectedUserName]
            except Exception : 
                validSubmission = False

            if validSubmission == True : 
                #create component object
                newLog = MaintenanceLog(logID=logID, datePerformed=selectedDatePerformed , action=enteredAction , userPerforming=selectedUser , component=selectedComp )

                #update components array in object utilities
                ObjectUtilities.addMaintenanceLog(newLog)

                #write to database 
                DatabaseManager.addLogToDatabase(newLog)
                
                messagebox.showinfo("Success!", "Action has been recorded.")
                addLogPopup.destroy()
            else :
                messagebox.showerror("Invalid Log", "Please ensure ID is unique and all fields have been filled.")

        #button to submit new component to be added
        submitComponentButton = ttk.Button(addLogPopup, text="Add Operational Log", command=submit)
        submitComponentButton.pack(pady=15)
      
#   ---------------------------------------------------------------------------
#   ---                       Show Component View Page                      ---
#   --- Displays all maintenance logs only relating to a specific component ---
#   ---------------------------------------------------------------------------
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


