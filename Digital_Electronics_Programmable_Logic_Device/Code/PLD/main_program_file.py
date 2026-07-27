import customtkinter as ctk
import tkinter.messagebox as mb
import os
from load_program_file import load_program
from create_program_file import create_program
from upload_program_file import upload_program
from edit_program_file import edit_program
from messagebox_file import messagebox
from test_program_file import test

def main_app(app):
    global heading_text, progress_bar, load_program_button, create_program_button, upload_program_button, edit_program_button
    progress_bar = ctk.CTkProgressBar(app)
    progress_bar.pack(pady=5)
    progress_bar.set(0)

    heading_text = ctk.CTkLabel(master=app,textvariable=app.program_var)
    heading_text.pack(pady=5)

    load_program_button = ctk.CTkButton(master=app,text="Load",command=lambda:load_program(app))
    load_program_button.pack(pady=10)

    create_program_button = ctk.CTkButton(master=app,text="Create",command=lambda:create_program(app))
    create_program_button.pack(pady=10)

    edit_program_button = ctk.CTkButton(master=app,text="Edit",command=lambda:edit_program(app))

    upload_program_button = ctk.CTkButton(master=app,text="Upload",command=lambda app=app, progress_bar=progress_bar:upload_program(app, progress_bar))

def clear_panel():
    global load_program_button, create_program_button
    load_program_button.pack_forget()
    create_program_button.pack_forget()

def set_program_panel(app):
    global progress_bar, test_button, delete_button, reset_button, heading_text, load_program_button, create_program_button, upload_program_button, edit_program_button
    clear_panel()
    progress_bar.set(1)
    app.program_var.set(app.program)
    edit_program_button.pack(pady=10)

    test_button = ctk.CTkButton(
        master=app,
        text="Test",
        command=lambda: test(app)
    )
    test_button.pack(pady=10)

    upload_program_button.pack(pady=10)

    reset_button = ctk.CTkButton(
        master=app,
        text="Remove",
        fg_color="#b36a03",       # Background color of button
        hover_color="#84520C",    # Color when mouse hovers
        command=lambda: reset(app)
    )
    reset_button.pack(pady=10)

    delete_button = ctk.CTkButton(
        master=app,
        text="Delete",
        fg_color="#df2020",       # Background color of button
        hover_color="#992828",    # Color when mouse hovers
        command=lambda: delete_program(app)
    )
    delete_button.pack(pady=10)

def delete_program(app):
    os.chdir(app.save_dir)
    if not os.path.exists(app.program):
        return
    if messagebox(app, "Delete Program", f"Are you sure you want to delete '{app.program}'?","Yes","No"):
        os.remove(app.program)
        reset(app)

def reset(app):
    global progress_bar, test_button, delete_button, reset_button, heading_text, load_program_button, create_program_button, upload_program_button, edit_program_button
    app.program = "No Program Selected"
    app.program_var.set(app.program)

    progress_bar.destroy()
    heading_text.destroy()
    load_program_button.destroy()
    create_program_button.destroy()
    upload_program_button.destroy()
    edit_program_button.destroy()
    reset_button.destroy()
    delete_button.destroy()
    test_button.destroy()
    main_app(app)