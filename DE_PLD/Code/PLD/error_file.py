# This file provides a function to create an error window when something goes wrong.

import customtkinter as ctk
import os

def error(app,desc="No details provided."):
    error_panel = ctk.CTkToplevel(app)
    error_panel.title("ERROR")
    error_panel.geometry("230x300")
    error_panel.resizable(False, False)

    # Make it behave like a modal dialog
    error_panel.transient(app)   # stay on top of parent
    error_panel.grab_set()       # block interaction with app
    error_panel.focus_force()

    # Center on parent
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - error_panel.winfo_width() // 2
    y = app.winfo_y() + (app.winfo_height() // 2) - error_panel.winfo_height() // 2
    error_panel.geometry(f"+{x}+{y}")

    error_label = ctk.CTkLabel(master=error_panel,text="An error has occured.")
    error_label.pack(pady=5)
    desc_label = ctk.CTkLabel(master=error_panel,text=desc,wraplength=error_panel.winfo_width() // 2)
    desc_label.pack(pady=5)

    close_button = ctk.CTkButton(master=error_panel,text="Okay",command=lambda:error_panel.destroy())
    close_button.pack(pady=5)