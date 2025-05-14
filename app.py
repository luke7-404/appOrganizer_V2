import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import os

JSON_FOLDER_PATH = (
    os.path.join(os.getenv("APPDATA"),"AppOrganizer")
)
JSON_FILE_PATH = (
    os.path.join(JSON_FOLDER_PATH, "apps.json")
)

def accessJSON(name: str, path: str):
    # This function will be used to access the JSON file
    # and load the apps into the window
    f = open(JSON_FILE_PATH, "r+")
    # if f.find("}") != -1:
    #     f.write(f'"{name}": "{path}"'.format())
    #     f.write("}")
    #     f.close()

def addAppToJSON():
  filePath = filedialog.askopenfilename( title="Select an app", 
                                           filetypes=[("Executable files", "*.exe"), 
                                                      ("Shortcuts", "*.lnk"), 
                                                      ("Batch files", "*.bat")])
  fileName = simpledialog.askstring("App Name", "Enter the name of the app:") 
  accessJSON(fileName, filePath)


def removeAppFromJSON():
  pass

def addAppToList():
  pass

def removeAppFromList():
  pass

def initWindow():
    # This function initializes the window
    print("Initializing window...")

    # Create a new window
    window = tk.Tk()

    # Set the title of the window
    window.title("App Organizer")

    # Set the size of the window
    window.geometry("400x300")
    window.resizable(False, False)

    # Add a label to the window
    tk.Label(window, text="Hello, World!").pack()

    tk.Button(window, text="Add App", command=lambda: addAppToJSON()).pack()
    tk.Button(window, text="Remove App", command=lambda: removeAppFromJSON()).pack()
    tk.Button(window, text="Change Icon").pack()

    return window


def loadApps():

  
  window.update
  
  pass

if __name__ == "__main__":
  
  if not os.path.exists(JSON_FILE_PATH):
    os.makedirs(JSON_FOLDER_PATH, exist_ok=True)
    with open(JSON_FILE_PATH, 'w') as f:
      f.write("{{}}".format())
    
  # Initialize the window (Add UI)
  window = initWindow()
  
  # Add apps to the window
  loadApps()
  
  # Run the window's event loop
  window.mainloop()
