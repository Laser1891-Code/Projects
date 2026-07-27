# This file provides the code to test a program digitally.
# This file was created with AI assistance. 

import customtkinter as ctk
import os
from generate_truthtable_file import create_truthtable
import copy

class core:
    def __init__(self):
        self.action = "NONE"
        self.input_1 = "0"
        self.input_2 = "0"     
        self.state = False  
    def reset(self): 
        self.action = "NONE"
        self.input_1 = "0"
        self.input_2 = "0" 
        self.state = False

class programableLogicDevice:
    def __init__(self):
        self.core_1 = core()
        self.core_2 = core()
        self.core_3 = core()
        self.core_4 = core()
        self.core_5 = core()
        self.core_6 = core()

class io_class:
    def __init__(self):
        self.A = False
        self.B = False
        self.C = False
        self.OUT = False

class circuit_class:
    def __init__(self):
        self.io = io_class()
        self.code = programableLogicDevice()

def get_code(app,pld):
    os.chdir(app.save_dir)
    with open(app.program, "r") as f:
        code = f.read()

    action_map = {
        "00": "AND",
        "10": "OR",
        "01": "INVERT"
    }

    input_map = {
        "000": "Input A",
        "100": "Input B",
        "010": "Input C",
        "110": "Core 1",
        "001": "Core 2",
        "101": "Core 3",
        "011": "Core 4",
        "111": "Core 5"
    }
    
    sections = code.split("|")
    for i in range(0,6):
        c = [pld.core_1, pld.core_2, pld.core_3, pld.core_4, pld.core_5, pld.core_6][i]
        section = sections[i]
        parts = section.split("-")
        c.input_2 = input_map.get(parts[0], "failed")
        c.input_1 = input_map.get(parts[1], "failed")
        c.action = action_map.get(parts[2], "NONE")

def simulate_circuit(circuit, output):
    on = "#16A500"
    off = "#df2020"

    # Map core names to actual state values
    def get_input_state(name):
        if name == "Input A":
            return circuit.io.A
        elif name == "Input B":
            return circuit.io.B
        elif name == "Input C":
            return circuit.io.C
        elif name == "Core 1":
            return circuit.code.core_1.state
        elif name == "Core 2":
            return circuit.code.core_2.state
        elif name == "Core 3":
            return circuit.code.core_3.state
        elif name == "Core 4":
            return circuit.code.core_4.state
        elif name == "Core 5":
            return circuit.code.core_5.state
        elif name == "Core 6":
            return circuit.code.core_6.state

    # Process cores in order
    cores = [
        circuit.code.core_1,
        circuit.code.core_2,
        circuit.code.core_3,
        circuit.code.core_4,
        circuit.code.core_5,
        circuit.code.core_6,
    ]

    for c in cores:
        a = get_input_state(c.input_1)
        b = get_input_state(c.input_2) if c.input_2 else False

        if c.action == "AND":
            c.state = a and b
        elif c.action == "OR":
            c.state = a or b
        elif c.action == "INVERT":
            c.state = not a
        else:
            c.state = False

    # Update output based on Core 6
    output.configure(fg_color=on if circuit.code.core_6.state else off)

def attempt_truthtable(app,panel,circuit):
    if app.truthtable == None:
        cloned_circuit = copy.deepcopy(circuit)
        create_truthtable(app,panel,cloned_circuit)

def destroy_panels(app,panel):
    if app.truthtable != None:
        app.truthtable.destroy()
        app.truthtable = None
    panel.destroy()

def test(app):
    test_panel = ctk.CTkToplevel(app)
    test_panel.title("Test Program")
    test_panel.geometry("230x300")
    test_panel.resizable(False, False)

    # Make it behave like a modal dialog
    test_panel.transient(app)
    test_panel.focus_force()

    # Center on parent
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - test_panel.winfo_width() // 2
    y = app.winfo_y() + (app.winfo_height() // 2) - test_panel.winfo_height() // 2
    test_panel.geometry(f"+{x}+{y}")

    circuit = circuit_class()
    get_code(app, circuit.code)

    heading_text = ctk.CTkLabel(master=test_panel, text="Testing: " + app.program)
    heading_text.pack(pady=5)

    output = ctk.CTkFrame(master=test_panel, width=50, height=50, fg_color="#8f8f8f")
    output.pack(pady=5)

    # Callback to update circuit inputs and simulate
    def update_output():
        simulate_circuit(circuit, output)

    update_output()

    # Switches
    var_A = ctk.BooleanVar(value=False)
    switch_A = ctk.CTkSwitch(
        master=test_panel,
        text="Input A",
        variable=var_A,
        command=lambda: (setattr(circuit.io, 'A', var_A.get()), update_output())
    )
    switch_A.pack(pady=5)

    var_B = ctk.BooleanVar(value=False)
    switch_B = ctk.CTkSwitch(
        master=test_panel,
        text="Input B",
        variable=var_B,
        command=lambda: (setattr(circuit.io, 'B', var_B.get()), update_output())
    )
    switch_B.pack(pady=5)

    var_C = ctk.BooleanVar(value=False)
    switch_C = ctk.CTkSwitch(
        master=test_panel,
        text="Input C",
        variable=var_C,
        command=lambda: (setattr(circuit.io, 'C', var_C.get()), update_output())
    )
    switch_C.pack(pady=5)

    close_button = ctk.CTkButton(master=test_panel, text="Truthtable", command=lambda app=app, circuit=circuit, test_panel=test_panel: attempt_truthtable(app, test_panel, circuit))
    close_button.pack(pady=10)

    close_button = ctk.CTkButton(master=test_panel, text="Close", command=lambda app=app, panel=test_panel: destroy_panels(app, panel))
    close_button.pack(pady=10)
