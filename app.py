import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import subprocess
import os

# Create a new window
WINDOW = tk.Tk()

# initializes the window
print("Initializing window...")

# Set the title of the window
WINDOW.title("App Organizer")

# Set the size of the window
WINDOW.geometry("400x300")
WINDOW.resizable(False, False)

# Add elements to the window
searchBar = ttk.Entry(WINDOW, width=35)
searchBar.grid(row=0, column=0, padx=2.5, pady=5)
tk.Button(WINDOW, text="Add App", command=lambda: addAppToJSON(), width=10).grid(row=0, column=1, padx=5, pady=5)
tk.Button(WINDOW, text="Remove App", command=lambda: removeAppFromJSON(), justify="right").grid(row=0, column=2, padx=5, pady=5)
ttk.Separator(WINDOW, orient="horizontal").grid(row=1, column=0, columnspan=30, sticky="ew", padx=5, pady=5)
l = tk.Listbox(WINDOW, listvariable={}, width=60, height=14)
l.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
s = ttk.Scrollbar(WINDOW, orient="vertical", command=l.yview)
s.grid(row=2, column=2, sticky="nse", padx=10)
l.configure(yscrollcommand=s.set)

JSON_FOLDER_PATH = (
    os.path.join(os.getenv("APPDATA"),"AppOrganizer")
)
JSON_FILE_PATH = (
    os.path.join(JSON_FOLDER_PATH, "apps.json")
)

# This function will add the app from the JSON file
def addAppToJSON():
    path = filedialog.askopenfilename( title="Select an app", 
                                           filetypes=[("All files", "*.*"),("Executable files", "*.exe"), 
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
        
        choicesVar.set(getNames()) # Update the listbox with the new app


# This function will remove the app from the JSON file
def removeAppFromJSON():
    selection = l.curselection()
    name = getNames()[selection[0]].lstrip()
    verify = None
    while True:
        verify = simpledialog.askstring(
            "Remove App", "To remove {" + name + "} from the list, type the name of the app to confirm",
        )
        if verify == name or verify == None:
            break

    if verify == name:
        contents = open(JSON_FILE_PATH, "r+").read().split(",")
        # print(contents)
        index = selection[0]
        # print(contents[index])
        # contents[index] = ""
        if index == len(contents) - 1: # if last element is selected
            contents.pop(index)
            contents[index-1] += "}"
        elif index == 0: # if first element is selected
            contents.pop(index)
            contents[index] = "{" + contents[index]
        else: # if any other element is selected
            contents.pop(index)

        # print(contents)
        f = open(JSON_FILE_PATH, "w")
        f.write(",".join(contents))
        f.close()

        choicesVar.set(getNames()) # Update the listbox with the new list

# This function will search for the app in the JSON file
def searchApp(evt):
    query = searchBar.get()
    filtered = []
    for i in getNames():
        if query.lower() in i.lower():
            filtered.append(i)
    choicesVar.set(filtered)

# Scrapes for the names
def getNames() -> list[str]:
    return [x.split(":")[0].replace('"', "").lstrip() for x in open(JSON_FILE_PATH).read()[1:-1].split(",") ] 

# Scrapes for the paths
def getPaths() -> list[str]:
    return [x.split(": ")[1].replace('"', "").lstrip() for x in open(JSON_FILE_PATH).read()[1:-1].split(",") ]

count = 0
previousSelection = None
# This function will load the apps from the JSON file
def loadApps():
    global count, previousSelection
    index = l.curselection()[0]
    try:
        path = os.path.normpath(getPaths()[index].lstrip())
        print(path)
        subprocess.Popen(path, shell=False)
        # WINDOW.quit()
    except Exception as e:
        print("Error: ", e)
        messagebox.showerror("Error", "Could not open the app. Error MSG: " + str(e))
        count = 0
        previousSelection = None

def on_select(event):
    global count, previousSelection
    if l.curselection()[0] == previousSelection:
        count += 1
    print(count)
    if count == 1:
        count = 0
        loadApps()
    previousSelection = l.curselection()[0]    


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

    choicesVar = tk.StringVar(value=getNames())
    l.config(listvariable=choicesVar)
    l.bind("<<ListboxSelect>>", on_select)
    searchBar.bind("<KeyRelease>", searchApp)

    # Run the window's event loop
    WINDOW.mainloop()
