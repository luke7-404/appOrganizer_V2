import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
import subprocess
import os

# Create a new window
WINDOW = tk.Tk()
choicesVar = None

JSON_FOLDER_PATH = (
    os.path.join(os.getenv("APPDATA"),"AppOrganizer")
)
JSON_FILE_PATH = (
    os.path.join(JSON_FOLDER_PATH, "apps.json")
)


def addAppToJSON():
    path = filedialog.askopenfilename( title="Select an app", 
                                           filetypes=[("Executable files", "*.exe"), 
                                                      ("Shortcuts", "*.lnk"), 
                                                      ("Batch files", "*.bat")])
    if not path == "":
        name = simpledialog.askstring("App Name", "Enter the name of the app:")
        f = open(JSON_FILE_PATH, "r+")
        contents = list(f.read())

        if len(contents) > 3:
            contents.insert(len(contents) - 1, ",")
        contents.insert(len(contents) - 1, (f'"{name}": "{path}"'.format()))
        f = open(JSON_FILE_PATH, "w")
        f.write("".join(contents))
        f.close()

def addAppToList():
  # foundApps = loadApps()
  # foundApps.append("App 21")
  # choicesVar.set(foundApps)
  pass
  # This function will add the app to the list

def removeAppFromJSON():
  pass
  # This function will remove the app from the JSON file

def removeAppFromList():
  pass
  # This function will remove the app from the list

def searchApp() -> list[str]:
    pass
    # This function will search for the app in the JSON file

def getNames() -> list[str]:
    # Scrapes for the names
    return [x.split(":")[0].replace('"', "") for x in open(JSON_FILE_PATH).read()[1:-1].split(",") ] 

def getPaths() -> list[str]:
    # Scrapes for the paths
    return [x.split(": ")[1].replace('"', "") for x in open(JSON_FILE_PATH).read()[1:-1].split(",") ]

def loadApps():
  pass
    # This function will load the apps from the JSON file

def initWindow():
    # This function initializes the window
    print("Initializing window...")
    
    # Set the title of the window
    WINDOW.title("App Organizer")

    # Set the size of the window
    WINDOW.geometry("400x300")
    WINDOW.resizable(False, False)

    # Add elements to the window
    ttk.Entry(WINDOW, width=35).grid(row=0, column=0, padx=2.5, pady=5)
    tk.Button(WINDOW, text="Add App", command=lambda: addAppToJSON(), width=10).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(WINDOW, text="Remove App", command=lambda: removeAppFromJSON(), justify="right").grid(row=0, column=2, padx=5, pady=5)
    ttk.Separator(WINDOW, orient="horizontal").grid(row=1, column=0, columnspan=30, sticky="ew", padx=5, pady=5)
    var = tk.StringVar(value=loadApps())
    l = tk.Listbox(WINDOW, listvariable=var, width=60, height=14)
    l.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
    s = ttk.Scrollbar(WINDOW, orient="vertical", command=l.yview)
    s.grid(row=2, column=2, sticky="nse", padx=10)
    l.configure(yscrollcommand=s.set)

    return var


if __name__ == "__main__":
    file_Obj = None

    if not os.path.exists(JSON_FILE_PATH):
        os.makedirs(JSON_FOLDER_PATH, exist_ok=True)
        file_Obj = open(JSON_FILE_PATH, "w")
        file_Obj.write("{{}}".format())
    else:
      file_Obj = open(JSON_FILE_PATH, "r+")
      
    if len(file_Obj.read()) == 0:
        file_Obj.write("{{}}".format())
        file_Obj.close()

    # Initialize the window (Add UI)
    choicesVar = initWindow()

    # Run the window's event loop
    WINDOW.mainloop()
