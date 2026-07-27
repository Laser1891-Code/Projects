# This file provides the functions to create a cancel confirmation pop-up.

import customtkinter as ctk
from messagebox_file import messagebox

def cancel_action(panel,confirmation):
    if confirmation:
        if messagebox(panel, "Cancel Action", "Are you sure you want cancel this action?","Yes","No"):
            panel.destroy()
    else:
        panel.destroy()

def cancel(panel,pad=20,confirmation=False):
    button = ctk.CTkButton(
        master=panel,
        text="Cancel",
        fg_color="#df2020",       # Background color of button
        hover_color="#992828",    # Color when mouse hovers
        command=lambda panel=panel, confirmation=confirmation: cancel_action(panel,confirmation)
    )
    button.pack(pady=pad)
    return button