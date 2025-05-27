import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import subprocess
import os

# Constants for the JSON file path
JSON_FOLDER_PATH = os.path.join(os.getenv("APPDATA"), "AppOrganizer")
JSON_FILE_PATH = os.path.join(JSON_FOLDER_PATH, "apps.json")

switched = False  # Global variable to track if the search paths are switched

# Create a new window and global widgets
WINDOW = tk.Tk()
searchBar = ttk.Entry(WINDOW, width=35)
settings = tk.Label(WINDOW, text="Settings", justify="right", width=10, pady=3.49, relief="raised")
l = tk.Listbox(WINDOW, listvariable={}, width=60, height=14)
s = ttk.Scrollbar(WINDOW, orient="vertical", command=l.yview)
menu = tk.Menu(WINDOW, tearoff=0)

# Scrapes for the names (keys) in the JSON file
def getNames() -> list[str]:
    return [
        x.split(":")[0].replace('"', "").lstrip() for x in open(JSON_FILE_PATH).read()[1:-1].split(",")
    ]


# Scrapes for the paths (values) in the JSON file
def getPaths() -> list[str]:
    return [
        x.split(": ")[1].replace('"', "").lstrip() for x in open(JSON_FILE_PATH).read()[1:-1].split(",")
    ]

# This function will add the app from the JSON file
def addAppToJSON():
    path = filedialog.askopenfilename(
        title="Select an app",
        filetypes=[
            ("All files", "*.*"),
            ("Executable files", "*.exe"),
            ("Shortcuts", "*.lnk"),
            ("Batch files", "*.bat"),
        ],
    )
    
    # if a file was selected
    if not path == "":
        name = simpledialog.askstring("App Name", "Enter the name of the app:")
        f = open(JSON_FILE_PATH, "r+")
        contents = list(f.read())

        # check if there are other apps in the JSON file if so add a comma 
        if len(contents) > 3:
            contents.insert(len(contents) - 1, ",")
            
        # format and insert the new app into the JSON file
        contents.insert(len(contents) - 1, (f'"{name}": "{path}"'.format()))
        f = open(JSON_FILE_PATH, "w")
        f.write("".join(contents))
        f.close()

        # if the listbox is disabled, enable it and update the listbox
        l.config(state="normal")
        choicesVar.set(itemType())  # Update the listbox with the new list

# This function will actually remove the app from the JSON file
def remove(evt):
    selection = evt.widget.curselection() # Get the selected item index

    name = itemType()[selection[0]].lstrip() # Get the name of the app to be removed
    verify = None
    
    # Ask the user to confirm the removal of the app
    while True:
        verify = simpledialog.askstring(
            "Remove App",
            "To remove {"
            + name
            + "} from the list, type the name of the app to confirm",
        )
        
        # if user entered the name of the app or clicked cancel exit the loop
        if verify == name or verify == None:
            break

    # if the user confirmed the removal of the app
    if verify == name:
        contents = open(JSON_FILE_PATH, "r+").read().split(",")
        index = selection[0]
        f = open(JSON_FILE_PATH, "w")
        
        if len(contents) == 1:  # if only one element is in the list
            f.write("{{}}".format())
            f.close()
        else:
            if index == len(contents) - 1:  # if last element is selected
                contents.pop(index)
                contents[index - 1] += "}"
            elif index == 0:  # if first element is selected
                contents.pop(index)
                contents[index] = "{" + contents[index]
            else:  # if any other element is selected
                contents.pop(index)

            # print(contents)
            f.write(",".join(contents))
            f.close()

        if itemType() == [""]:  # if only one element is in the list
            evt.widget.winfo_toplevel().destroy()
            l.config(state="disabled") # Disable the listbox if no apps are left
        choicesVar.set(itemType())  # Update the listbox with the new list

# This function will open a new window to remove an app from the JSON file
def removeAppFromJSON():
    if itemType() == [""]: # if there are no apps in the list then do not open the window
        return

    # Create a new popup window for removing apps
    toplevel = tk.Toplevel(WINDOW)
    toplevel.title("Remove App")
    toplevel.geometry("300x100")
    toplevel.resizable(False, False)
    removelb = tk.Listbox(toplevel, listvariable=choicesVar, width=60, height=14)
    removelb.pack(padx=5, pady=5)

    removelb.bind("<<ListboxSelect>>", remove)

    # Make the popup window modal
    toplevel.grab_set()  
    WINDOW.wait_window(toplevel)

# This function will search for the app in the JSON file
def searchApp(evt):
    query = searchBar.get()
    filtered = []
    for i in itemType():
        # if the query is in the app name then add it to the filtered list
        # case insensitive search
        if query.lower() in i.lower():
            filtered.append(i)
    choicesVar.set(filtered) # Update the listbox with the filtered list

def itemType() -> list[str]:
    if switched:
        return getPaths()
    return getNames()

def switchItemType():
    global switched
    switched = not switched  # Toggle the switched variable
    choicesVar.set(itemType())  # Update the listbox with the new list

# This function will load the apps from the JSON file
def loadApps(evt):
    try: # Get the selected item and open the app``
        index = evt.widget.curselection()[0]
        path = os.path.normpath(getPaths()[index].lstrip())
        print(path)
        subprocess.Popen(path, shell=False)
        WINDOW.quit()
    except Exception as e: # If there is an error opening the app, show an error message
        print("Error: ", e)
        messagebox.showerror("Error", "Could not open the app. Error MSG: " + str(e))

# This function will show the context menu when clicking on the settings button
def show_menu(event):
    try:
        menu.tk_popup(event.x_root, event.y_root) # Show the menu
    finally:
        menu.grab_release() # Release the grab so the menu can be closed

# initializes the window and its widgets
def initWidgets():
    print("Initializing window...")

    # Set the title of the window
    WINDOW.title("App Organizer")

    # Set the size of the window
    WINDOW.geometry("400x300")
    WINDOW.resizable(False, False)

    # Add elements to the window

    tk.Button(WINDOW, text="Add App", command=lambda: addAppToJSON(), width=10).grid(
        row=0, column=1, padx=5, pady=5
    )
    ttk.Separator(WINDOW, orient="horizontal").grid(
        row=1, column=0, columnspan=30, sticky="ew", padx=5, pady=5
    )

    searchBar.grid(row=0, column=0, padx=2.5, pady=5)
    settings.grid(row=0, column=2, padx=5, pady=5)
    l.grid(row=2, column=0, columnspan=3, padx=0, pady=5)
    s.grid(row=2, column=2, sticky="nse", padx=15)

    l.configure(yscrollcommand=s.set)

    l.bind("<<ListboxSelect>>", loadApps)
    searchBar.bind("<KeyRelease>", searchApp)
    settings.bind("<Button-1>", show_menu)

    menu.add_command(label="Remove App", command=lambda: removeAppFromJSON())
    menu.add_command(label="Open JSON", command=lambda: os.startfile(JSON_FILE_PATH))
    menu.add_command(label="Search Paths", command=lambda: switchItemType())

# main
if __name__ == "__main__":
    file_Obj = None

    # Check if the JSON file exists, if not create it
    if not os.path.exists(JSON_FILE_PATH):
        os.makedirs(JSON_FOLDER_PATH, exist_ok=True)
        file_Obj = open(JSON_FILE_PATH, "w")
        file_Obj.write("{{}}".format())
    else: # If the file exists, check if it is empty
        file_Obj = open(JSON_FILE_PATH, "r+")
        if len(file_Obj.read()) == 0: # if the file is empty, add {}
            file_Obj.write("{{}}".format())
            file_Obj.close()

    # init the listbox with the names from the JSON file
    choicesVar = tk.StringVar(value=itemType())
    
    # If there are no apps in the JSON file, disable the listbox
    if choicesVar.get() == "('',)":
        l.config(state="disabled")
    l.config(listvariable=choicesVar) # update listbox
    
    initWidgets()  # Initialize the widgets

    # Run the window's event loop
    WINDOW.mainloop()
