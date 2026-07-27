import customtkinter as ctk
from error_file import error
from program_program_file import program_gui


def edit_program(app):
    edit_panel = ctk.CTkToplevel(app)
    edit_panel.title("Edit Program")
    edit_panel.geometry("230x350")
    edit_panel.resizable(False, False)

    # Make it behave like a modal dialog
    edit_panel.transient(app)   # stay on top of parent
    edit_panel.grab_set()       # block interaction with app
    edit_panel.focus_force()

    # Center on parent
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - edit_panel.winfo_width() // 2
    y = app.winfo_y() + (app.winfo_height() // 2) - edit_panel.winfo_height() // 2
    edit_panel.geometry(f"+{x}+{y}")

    program_gui(app,edit_panel)


