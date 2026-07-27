import customtkinter as ctk
import os
from cancel_funciton_file import cancel

def load(app, panel):
    if app.program != "No Program Selected":     
        from main_program_file import set_program_panel
        panel.destroy()
        set_program_panel(app)

def load_program(app):
    load_panel = ctk.CTkToplevel(app)
    load_panel.title("Load Program")
    load_panel.geometry("230x300")
    load_panel.resizable(False, False)

    # Make it behave like a modal dialog
    load_panel.transient(app)   # stay on top of parent
    load_panel.grab_set()       # block interaction with app
    load_panel.focus_force()

    # Center on parent
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - load_panel.winfo_width() // 2
    y = app.winfo_y() + (app.winfo_height() // 2) - load_panel.winfo_height() // 2
    load_panel.geometry(f"+{x}+{y}")

    heading_text = ctk.CTkLabel(master=load_panel,text="Select a Program")
    heading_text.pack(pady=5)

    programs_raw = os.listdir(app.save_dir)
    programs = []
    for folder in programs_raw:
        if not folder == "Arduino15" and not folder == "sketches":
            programs.append(folder)
    
    def combobox_callback(choice):
        app.program = choice

    program_combobox = ctk.CTkComboBox(load_panel, values=programs,command=combobox_callback)
    program_combobox.pack(pady=5)
    program_combobox.set("None")

    load_program_button = ctk.CTkButton(master=load_panel,text="Load",command=lambda:load(app,load_panel))
    load_program_button.pack(pady=5)

    cancel(load_panel)

    


