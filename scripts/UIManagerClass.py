from tkinter import *
from tkinter import messagebox, ttk
from functools import partial
from ObjectUtilitiesClass import ObjectUtilities
from ComponentClass import StatusT, Component
from MaintenanceLogClass import MaintenanceLog
from LocationClass import Location, LocationT
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

        inventoryView = Menu(menu, tearoff=0)
        inventoryView.add_command(label="View Components", command=UIManager.showInventoryPage)
        inventoryView.add_command(label="Search Components", command=UIManager.showComponentViewPage)
        inventoryView.add_cascade(label="View Maintenance Logs", command=UIManager.showMaintenanceLogs)
        inventoryView.add_cascade(label="View Locations", command=UIManager.showLocationsPage)
        inventoryView.add_cascade(label="View Users", command=UIManager.showUsersPage)

        inventoryAdd = Menu(menu, tearoff=0)
        inventoryAdd.add_command(label="Add Component", command=UIManager.addComponentPage)
        inventoryAdd.add_command(label="Add Log Entry", command=UIManager.addLogPage) 
        inventoryAdd.add_command(label="Add Location", command=UIManager.addLocationPage)
        inventoryAdd.add_command(label="Add User", command=root.destroy) #NEED TO ADD COMMAND

        menu.add_cascade(label="Add", menu=inventoryAdd)
        menu.add_cascade(label="Inventory View", menu=inventoryView)
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

        #maintenance logs title
        titleLabel = Label(root, text="Maintenance Logs")
        titleLabel.pack(pady=5)

        #creates frame to holder the table and scroll bar
        frame = UIManager.maintenanceLogTableFrame(root, None)
        root.mainloop()

    @classmethod
    def maintenanceLogTableFrame(cls, root, selectedComponent) :
        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #component table created with column headers
        treeView = ttk.Treeview(frame, columns=("LogID", "Component", "Action", "Date", "User"), show="headings")

        #prints headers
        for col in ("LogID", "Component", "Action", "Date", "User") :
            treeView.heading(col, text=col)
            treeView.column(col, anchor="center", stretch=True, width=100)

        if selectedComponent == None :
            pass #meaning show all

        #displays loaded components in table
        for maintenanceLog in range(ObjectUtilities.getNumLogs()) :
            log = ObjectUtilities.getLog(maintenanceLog)
            if selectedComponent == None :
                treeView.insert("", "end", values=(str(log.getLogID()), str(log.getComponent().getComponentID()), str(log.getAction()), str(log.getDatePerformed()), log.getUserPerforming().getName()))
            elif log.getComponent() == selectedComponent :
                    treeView.insert("", "end", values=(str(log.getLogID()), str(log.getComponent().getComponentID()), str(log.getAction()), str(log.getDatePerformed()), log.getUserPerforming().getName()))

        #scrollbar 
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeView.yview)
        treeView.configure(yscrollcommand=scrollbar.set)

        treeView.pack(padx=5, pady=5, expand=True)

        return frame

#   ---------------------------------------------------------------------------
#   ---                       Show Component View Page                      ---
#   --- Displays all maintenance logs only relating to a specific component ---
#   ---------------------------------------------------------------------------
    @classmethod
    def showComponentViewPage(cls) : 
        root = UIManager.createWindowMenu()
        currentLogFrame = None
        
        #creates container for component search:
        searchFrame = Frame(root)
        searchFrame.pack(expand=True)

        #dropdown to select a component to view
        compLabel = Label(searchFrame, text="Select Component ID:")
        compLabel.pack(pady=5)

        components = {}
        for comp in range(ObjectUtilities.getNumComponents()) : 
            component = ObjectUtilities.getComponent(comp)
            components[component.getComponentID()] = component
        componentSelect = ttk.Combobox(searchFrame, values=list(components.keys()), state="readonly")
        componentSelect.pack()

        def submit() :
            #gets component from box
            selectedComponentID = int(componentSelect.get())

            validSubmission = True

            try :
                selectedComp = components[selectedComponentID]
            except Exception :
                validSubmission = False

            if validSubmission :
                nonlocal currentLogFrame

                #creates table frame
                logFrame = UIManager.maintenanceLogTableFrame(root=root, selectedComponent=selectedComp)

                #destroys old table every button press so several components can be searched
                if currentLogFrame is not None :
                    currentLogFrame.destroy()

                #creates new table
                currentLogFrame = logFrame
                currentLogFrame.pack(pady=5)

            else :
                messagebox.showerror("Invalid Entry", "Please select a component to search.")

        #button to submit search
        searchButton = Button(searchFrame, text="Search", command=submit)
        searchButton.pack(pady=5)

        root.mainloop()

#   ---------------------------------------------------------
#   ---                Show Locations Page                ---
#   --- Displays locations currently loaded in at runtime ---
#   ---------------------------------------------------------
    @classmethod
    def showLocationsPage(cls) :
        #gets route window with standardised title and menu bar
        root = UIManager.createWindowMenu()

        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #title label
        locationsLabel = Label(frame, text="Locations")
        locationsLabel.pack(pady=5)

        #location table created with column headers
        treeView = ttk.Treeview(root, columns=("LocationID", "Name", "Type", "Postcode"), show="headings")

        #prints headers
        for col in ("LocationID", "Name", "Type", "Postcode") :
            treeView.heading(col, text=col)
            treeView.column(col, anchor="center", stretch=True, width=100)

        #displays loaded locations in table
        for location in range(ObjectUtilities.getNumLocations()) :
            loc = ObjectUtilities.getLocation(location)
            treeView.insert("", "end", values=(str(loc.getLocationID()), str(loc.getName()), loc.getLocationType().name, loc.getPostcode()))

        #scrollbar 
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeView.yview)
        treeView.configure(yscrollcommand=scrollbar.set)

        treeView.pack(padx=5, pady=5, expand=True)
        root.mainloop()

#   -----------------------------------------------------
#   ---                Show Users Page                ---
#   --- Displays users currently loaded in at runtime ---
#   -----------------------------------------------------
    @classmethod
    def showUsersPage(cls) :
        #gets route window with standardised title and menu bar
        root = UIManager.createWindowMenu()

        #creates frame to holder the table and scroll bar
        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True)

        #title label
        usersLabel = Label(frame, text="Users")
        usersLabel.pack(pady=5)

        #user table created with column headers
        treeView = ttk.Treeview(root, columns=("UserID", "Name", "Role"), show="headings")

        #prints headers
        for col in ("UserID", "Name", "Role") :
            treeView.heading(col, text=col)
            treeView.column(col, anchor="center", stretch=True, width=100)

        #displays loaded users in table
        for user in range(ObjectUtilities.getNumUsers()) :
            usr = ObjectUtilities.getUser(user)
            if usr.getIsManager() :
                role = "MANAGER"
            else :
                role = "ENGINEER"

            treeView.insert("", "end", values=(str(usr.getUserID()), usr.getName(), role))

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

            #gets date through series of try catches to ensure day month and year have all been selected
            try :
                selectedDay = dayBox.get()
                if selectedDay == "" :
                    validSubmission = False
            except Exception :
                validSubmission = False

            #gets month from box
            try :
                selectedMonth = monthBox.get()
                if selectedMonth == "" :
                    validSubmission = False
            except Exception :
                validSubmission = False

            #gets year from box
            try :
                selectedYear = yearBox.get()
                if selectedYear == "" :
                    validSubmission = False
            except Exception :                    
                validSubmission = False

            #forms whole date
            selectedDatePerformed = str(selectedDay) + "/" + str(selectedMonth) + "/" + str(selectedYear)

            #gets action performed 
            enteredAction = actionEntry.get()
            if enteredAction == "" :
                    validSubmission = False
            
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

#   -----------------------------------------------------------------------------------------
#   ---                                 Add Location Page                                 ---
#   --- Provides popup and authenticates new location, then requests addition to database ---
#   -----------------------------------------------------------------------------------------
    @classmethod
    def addLocationPage(cls) : 
        #creates popup to enter component details
        addLocationPopup = Toplevel()
        addLocationPopup.title("Add Location")
        addLocationPopup.geometry("300x500")
        addLocationPopup.resizable(False, False)

        #location ID label and input box
        locationIDLabel = Label(addLocationPopup, text="Location ID:")
        locationIDLabel.pack(pady=5)
        locationID = StringVar()
        locationIDEntry = Entry(addLocationPopup, textvariable=locationID)
        locationIDEntry.pack(pady=5)

        def verifyUniqueLocationID(userInput) :
            try :
                userInput = int(userInput)
                if userInput > 0 :
                    for loc in range(ObjectUtilities.getNumLocations()) :
                        if ObjectUtilities.getLocation(loc).getLocationID() == userInput :
                            return -1
                    #has exited for statement:
                    return userInput
                else :
                    return -1
            except Exception :
                return -1

        #location name label and input box
        locNameLabel = Label(addLocationPopup, text="Location Name:")
        locNameLabel.pack(pady=5)
        locName = StringVar()
        locNameEntry = Entry(addLocationPopup, textvariable=locName) #needs to be turned upper case
        locNameEntry.pack(pady=5)

        #location type label and input box / drop down
        locationTypeLabel = Label(addLocationPopup, text="Location Type:")
        locationTypeLabel.pack(pady=5)
        locTypeNames = []
        for type in LocationT :
            locTypeNames.append(type.name)
        typeSelect = ttk.Combobox(addLocationPopup, values=locTypeNames, state="readonly")
        typeSelect.pack()

        #location postcode label and input box 
        postcodeLabel = Label(addLocationPopup, text="Postcode:")
        postcodeLabel.pack(pady=5)
        postcode = StringVar()
        postcodeEntry = Entry(addLocationPopup, textvariable=postcode) #needs to be turned upper case
        postcodeEntry.pack(pady=5)

        #embedded submit function to be executed on button click
        def submit() :
            validSubmission = True
            
            #gets location ID
            selectedLocationID = verifyUniqueLocationID(locationIDEntry.get())
            if selectedLocationID == -1 :
                validSubmission = False

            #gets component type
            selectedLocationName = locNameEntry.get().upper()
            if selectedLocationName == "" :
                validSubmission = False
            
            #gets status from box
            selectedLocationTypeName = typeSelect.get()
            try :
                selectedLocType = LocationT[selectedLocationTypeName]
            except Exception :
                validSubmission = False

            #gets location from dropdown box
            selectedLocationPostcode = postcodeEntry.get().upper()
            if selectedLocationPostcode == "" :
                validSubmission = False

            if validSubmission == True : 
                #create location object
                newLocation = Location(locationID=selectedLocationID, name=selectedLocationName, locationType=selectedLocType, postcode=selectedLocationPostcode)

                #update locations array in object utilities
                ObjectUtilities.addLocation(newLocation)

                #write to database 
                DatabaseManager.addLocationToDatabase(newLocation)
                
                messagebox.showinfo("Success!", "Location has been added to inventory.")
                addLocationPopup.destroy()
            else :
                messagebox.showerror("Invalid Location", "Please ensure ID is unique and quantities are positive integers.")

        #button to submit new component to be added
        submitLocationButton = ttk.Button(addLocationPopup, text="Add Location", command=submit)
        submitLocationButton.pack(pady=15)
    
