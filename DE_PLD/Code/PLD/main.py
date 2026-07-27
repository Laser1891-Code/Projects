# This file sets up the entire program.

import customtkinter as ctk
import os
from main_program_file import main_app

os.system('cls')

# Save files to APPDATA/roaming/Custom-PLD-Programmar/Saved-Programs
SAVE_DIR = os.path.join(
    os.getenv("APPDATA"),
    "Custom-PLD-Programmer",
    "Saved-Programs"
)
#script_dir = os.path.dirname(os.path.abspath(__file__))
#SAVE_DIR = os.path.join(script_dir,"Saved Programs")
os.makedirs(SAVE_DIR, exist_ok=True)
os.chdir(SAVE_DIR)

with open("../info.txt","w") as f:
    f.write("This is the file storage area for the Custom PLD Programmer (CPLDP). Deleting these files/this folder won't break the program. It is automatically generated at the start of running the executable version of this program. - Ralph")

import os

try:
    os.makedirs("sketches", exist_ok=True)
    os.makedirs("sketches/PLD", exist_ok=True)
    with open("sketches/PLD/PLD.ino", "w") as f:
        f.write("")
except Exception as e:
    print(e)


ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')
app = ctk.CTk()
app.title("CPLDP")
app.geometry("230x300")
app.resizable(False, False)
app.program = "No Program Selected"
app.program_var = ctk.StringVar(value=app.program)
app.save_dir = SAVE_DIR
app.truthtable = None
main_app(app)
app.mainloop()