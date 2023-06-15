import platform
import tkinter as tk
from addondownloader import AddonDownloader
from pathlib import Path
from threading import Thread
from tkinter import filedialog
from tkinter import ttk
from screeninfo import get_monitors

def touch_file(filename):
    """Makes sure file exists"""
    filename = Path(filename)
    filename.touch(exist_ok=True)
    return filename

def create_addon_files():
    addons_file = open(touch_file("addons.txt"), "r+")
    addons_location_file = open(touch_file("addonslocation.txt"), "r+")
    addons = addons_file.read()
    addons_location = addons_location_file.read()
    if addons_location == "":
        if platform.system() == "Windows":
            addons_location = str(Path.home()) + "/Documents/Elder Scrolls Online/live/AddOns"
        else:
            addons_location = str(Path.home()) + "/.local/share/Steam/steamapps/compatdata/306130/pfx/drive_c/users/steamuser/Documents/Elder Scrolls Online/live/AddOns"
    addons_file.close()
    addons_location_file.close()
    return addons_location, addons

def update_status_text(text):
    status_label.config(text=text)

def on_start_download():
    #Save all the input data to text files
    #ESO addon location folder
    addons_location_file = open("addonslocation.txt", "w")
    addons_location_file.write(addons_location_field.get("1.0", "end-1c"))
    addons_location_file.close()
    #List of links
    addons = open("addons.txt", "w")
    textbuffer = addon_link_textview.get("1.0", "end-1c")
    addons.write(textbuffer)
    addons.close()

    adlthread = Thread(target=adl.start)
    handle_thread(adlthread)

def handle_thread(thread):
    thread.daemon = True
    try:
        thread.start()
    except Exception as err:
        update_status_text(str(err))


addons_location, addons = create_addon_files()
adl = AddonDownloader(update_status_text)

# GUI starts here!
#ESO_tk = ThemedTk(theme="breeze")
ESO_tk = tk.Tk()
ESO_tk.title("ESO Addon Downloader")
ESO_tk.iconphoto(False, tk.PhotoImage(file="esotux.png"))
ESO_tk.geometry("500x500")
ESO_tk.minsize(500, 500)
ESO_tk.grid_columnconfigure(0, weight=1)
ESO_tk.grid_rowconfigure(4, weight=1)
# Addons location
addonslbl = ttk.Label(text="ESO Addon folder location")
addons_location_field = tk.Text(height=1, wrap="none")
addons_location_field.insert(tk.END, addons_location)

def select_directory():
    addons_location = filedialog.askdirectory(title="Select Addons Directory", initialdir=addons_location_field.get("1.0", "end-1c"))
    addons_location_field.delete("1.0", tk.END)
    addons_location_field.insert(tk.END, addons_location)

aobutton = ttk.Button(text="Select", command=select_directory)
addonslbl.grid(row=0, column=0, sticky="w")
addons_location_field.grid(row=1, column=0, sticky="ew")
aobutton.grid(row=2, column=0, sticky="ew")

# Addons links
addonslinkslbl = ttk.Label(text="Links to ESOUI.com addon pages, one per line")
addon_link_textview = tk.Text(wrap="none")
addon_link_textview.insert(tk.END, addons)
addonslinkslbl.grid(row=3, column=0, sticky="w")
addon_link_textview.grid(row=4, column=0, sticky="nsew")

# Downlaod button
dlButton = ttk.Button(text="Download", command=on_start_download)
dlButton.grid(row=5, column=0, sticky="ew")

# Status bar
status_label = tk.Label(text="Ready to download...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=6, column=0, sticky="ew")

#Setup for centering the window on main monitor
ESO_tk.update_idletasks()
# Gets the requested values of the height and width.
windowWidth = ESO_tk.winfo_width()
windowHeight = ESO_tk.winfo_height()

# Positions the window in the center of the page.
ESO_tk.geometry(f"{windowWidth}x{windowHeight}+{(get_monitors()[0].width - windowWidth)//2}+{(get_monitors()[0].height - windowHeight)//2}")

if __name__ == "__main__":
    ESO_tk.mainloop()

