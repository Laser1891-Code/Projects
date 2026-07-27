import customtkinter as ctk
import os

def simulate_circuit(circuit):
    input_map = {
        "Input A": 0,
        "Input B": 1,
        "Input C": 2,
        "Core 1": 3,
        "Core 2": 4,
        "Core 3": 5,
        "Core 4": 6,
        "Core 5": 7,
    }

    cores = [
        circuit.code.core_1,
        circuit.code.core_2,
        circuit.code.core_3,
        circuit.code.core_4,
        circuit.code.core_5,
        circuit.code.core_6,
    ]

    # iterate until stable
    while True:
        changed = False

        snapshot = [
            circuit.io.A,
            circuit.io.B,
            circuit.io.C,
            circuit.code.core_1.state,
            circuit.code.core_2.state,
            circuit.code.core_3.state,
            circuit.code.core_4.state,
            circuit.code.core_5.state,
        ]

        for c in cores:
            if c.action == "AND":
                new_state = (
                    snapshot[input_map[c.input_1]]
                    and snapshot[input_map[c.input_2]]
                )
            elif c.action == "OR":
                new_state = (
                    snapshot[input_map[c.input_1]]
                    or snapshot[input_map[c.input_2]]
                )
            elif c.action == "INVERT":
                new_state = not snapshot[input_map[c.input_1]]
            else:
                new_state = True

            if new_state != c.state:
                c.state = new_state
                changed = True

        if not changed:
            break  # circuit settled

    return circuit.code.core_6.state

def reset_cores(circuit):
    for c in (
        circuit.code.core_1,
        circuit.code.core_2,
        circuit.code.core_3,
        circuit.code.core_4,
        circuit.code.core_5,
        circuit.code.core_6,
    ):
        c.state = False

def bits_from_int(n):
    return bool(n & 1), bool(n & 2), bool(n & 4)

def lock_windows(left, right, offset_x=10, offset_y=0):
    def sync(_=None):
        if not right.winfo_exists():
            return
        x = left.winfo_x() + left.winfo_width() + offset_x
        y = left.winfo_y() + offset_y
        right.geometry(f"+{x}+{y}")

    left.bind("<Configure>", sync)
    sync()



def create_truthtable(app, panel, circuit):
    truthtable_panel = ctk.CTkToplevel(app)
    truthtable_panel.title("Truth Table")
    truthtable_panel.geometry("230x300")
    truthtable_panel.resizable(False, False)
    truthtable_panel.focus_force()
    app.truthtable = truthtable_panel
    lock_windows(panel, truthtable_panel)


    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - truthtable_panel.winfo_width() // 2
    y = app.winfo_y() + (app.winfo_height() // 2) - truthtable_panel.winfo_height() // 2
    truthtable_panel.geometry(f"+{x}+{y}")

    on = "#16A500"
    off = "#df2020"

    truthtable = []

    header_frame = ctk.CTkFrame(master=truthtable_panel, height=25)
    header_frame.pack(fill="x", pady=4, padx=4)
    header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    col_A = ctk.CTkFrame(master=header_frame,width=20,height=20,fg_color="#2b2b2b")
    col_A.grid(row=0, column=0, padx=5)
    label_A = ctk.CTkLabel(master=col_A,text="A")
    label_A.pack()

    col_B = ctk.CTkFrame(master=header_frame,width=20,height=20,fg_color="#2b2b2b")
    col_B.grid(row=0, column=1, padx=5)
    label_B = ctk.CTkLabel(master=col_B,text="B")
    label_B.pack()

    col_C = ctk.CTkFrame(master=header_frame,width=20,height=20,fg_color="#2b2b2b")
    col_C.grid(row=0, column=2, padx=5)
    label_C = ctk.CTkLabel(master=col_C,text="C")
    label_C.pack()

    col_O = ctk.CTkFrame(master=header_frame,width=20,height=20,fg_color="#2b2b2b")
    col_O.grid(row=0, column=3, padx=5)
    label_O = ctk.CTkLabel(master=col_O,text="O")
    label_O.pack()


    for i in range(8):
        A, B, C = bits_from_int(i)

        circuit.io.A = A
        circuit.io.B = B
        circuit.io.C = C

        reset_cores(circuit)

        out = simulate_circuit(circuit)
        truthtable.append([A, B, C, out])

    for row in truthtable:
        row_frame = ctk.CTkFrame(master=truthtable_panel, height=25, fg_color="transparent", bg_color="transparent")
        row_frame.pack(fill="x", pady=4)
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for i, slot in enumerate(row):
            col = ctk.CTkFrame(
                master=row_frame,
                width=20,
                height=20,
                fg_color=on if slot else off,
            )
            col.grid(row=0, column=i, padx=5)

    def close(app):
        app.truthtable.destroy()
        app.truthtable = None


    close_button = ctk.CTkButton(
        master=truthtable_panel,
        text="Close",
        command=lambda app=app: close(app)
    )
    close_button.pack(pady=10)
