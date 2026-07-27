import customtkinter as ctk

def messagebox(app, title, desc, choice_1, choice_2):
    result = {"value": None}  # store the result

    messagebox_panel = ctk.CTkToplevel(app)
    messagebox_panel.title("Important Message")
    messagebox_panel.geometry("230x150")
    messagebox_panel.resizable(False, False)

    # Modal behavior
    messagebox_panel.transient(app)
    messagebox_panel.grab_set()
    messagebox_panel.focus_force()

    # Center on parent
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - messagebox_panel.winfo_width() // 2
    y = app.winfo_y() + (app.winfo_height() // 2) - messagebox_panel.winfo_height() // 2
    messagebox_panel.geometry(f"+{x}+{y}")

    # Text
    ctk.CTkLabel(master=messagebox_panel, text=title).pack(pady=5)
    ctk.CTkLabel(master=messagebox_panel, text=desc, wraplength=200).pack(pady=5)

    # Button callbacks
    def choice_1_callback():
        result["value"] = True
        messagebox_panel.destroy()

    def choice_2_callback():
        result["value"] = False
        messagebox_panel.destroy()

    # Buttons
    button_frame = ctk.CTkFrame(messagebox_panel,bg_color="#2b2b2b")
    button_frame.pack(pady=10)
    button_frame.grid_columnconfigure((0, 1), weight=1)

    if choice_2:
        ctk.CTkButton(button_frame, text=choice_1, width=80, command=choice_1_callback).grid(row=0, column=0, padx=5)
        ctk.CTkButton(button_frame, text=choice_2, width=80, command=choice_2_callback).grid(row=0, column=1, padx=5)
    else:
        ctk.CTkButton(button_frame, text=choice_1, width=80, command=choice_1_callback).grid(padx=5)
    # Wait until the modal is closed
    app.wait_window(messagebox_panel)

    return result["value"]
