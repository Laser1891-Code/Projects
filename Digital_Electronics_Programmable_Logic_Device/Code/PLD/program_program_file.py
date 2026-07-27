import customtkinter as ctk
from cancel_funciton_file import cancel
from safe_filename_file import safe_filename
from error_file import error
import os

def save(app,panel,new_name,name_textbox,pld):
    os.chdir(app.save_dir)
    safe_name = safe_filename(app, new_name,overwrite=True)
    if safe_name != "":
        try:    
            # Rename the program.
            os.rename(app.program, safe_name)
            name_textbox.delete(0, "end")
            name_textbox.insert(0,safe_name)
            app.program = safe_name
            app.program_var.set(app.program)
            try:
                # Map actions to codes
                action_map = {
                    "AND": "00",
                    "OR": "10",
                    "INVERT": "01"
                }
                # Map inputs to codes
                input_map = {
                    "Input A": "000",
                    "Input B": "100",
                    "Input C": "010",
                    "Core 1": "110",
                    "Core 2": "001",
                    "Core 3": "101",
                    "Core 4": "011",
                    "Core 5": "111"
                }

                # Add input codes
                output_string = ""
                for c in [pld.core_1, pld.core_2, pld.core_3, pld.core_4, pld.core_5, pld.core_6]:
                    output_string += f"{input_map.get(c.input_2,'000')}-{input_map.get(c.input_1,'000')}-{action_map.get(c.action, '11')}|"
                # Remove trailing '|'
                output_string = output_string.rstrip('|')
    
                with open(app.program, "w") as f:
                    f.write(output_string)

                pld.core_1.reset()
                pld.core_2.reset()
                pld.core_3.reset()
                pld.core_4.reset()
                pld.core_5.reset()
                pld.core_6.reset()
            except:
                error(app, "Error saving data to the program.")

            panel.destroy()
        except:
            error(app, "Error saving the program. Maybe try another name? Names cannot repeat.")

class core:
    def __init__(self):
        self.action = "NONE"
        self.input_1 = "0"
        self.input_2 = "0"       
    def reset(self): 
        self.action = "NONE"
        self.input_1 = "0"
        self.input_2 = "0" 

class programableLogicDevice:
    def __init__(self):
        self.core_1 = core()
        self.core_2 = core()
        self.core_3 = core()
        self.core_4 = core()
        self.core_5 = core()
        self.core_6 = core()

class editing_class:
    def __init__(self):
        self.editing = True
        self.core_num = 0
        self.past_core_num = 0
        self.progress_values = []
        split_val = 1/5
        for i in range(0,6): 
            self.progress_values.append(split_val*i)

editing = editing_class()

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

def program_gui(app,panel):
    global editing
    pld = programableLogicDevice()
    operations = ["AND","OR","INVERT","NONE"]
    inputs = ["Input A","Input B","Input C","Core 1","Core 2","Core 3","Core 4","Core 5"]

    program_name = ctk.CTkEntry(master=panel, placeholder_text="Program Name...")
    program_name.insert(0, app.program)
    program_name.pack(pady=5)

    def pld_callback(choice, core, type):
        core_attr = getattr(pld, f"core_{core}")
        if type == 1: core_attr.action = choice
        elif type == 2: core_attr.input_1 = choice
        elif type == 3: core_attr.input_2 = choice

    core_box = ctk.CTkFrame(
        master=panel,
        width=panel.winfo_width() // 2,
        height=panel.winfo_height() // 2 - 100,
        fg_color="transparent",
        bg_color="transparent"
    )
    core_box.pack(fill="both", expand=True, pady=5)

    progress = ctk.CTkProgressBar(master=core_box,width=300)
    progress.set(0)
    progress.pack(pady=5)

    get_code(app,pld)

    cores = []
    for c in range(1,7):
        c_obj = [pld.core_1, pld.core_2, pld.core_3, pld.core_4, pld.core_5, pld.core_6][c-1]
        core_action_label = ctk.CTkLabel(master=core_box,text="Core " + str(c) + ": Action")
        core_action_combobox = ctk.CTkComboBox(core_box, values=operations,command=lambda choice, c=c: pld_callback(choice, c, 1))
        core_action_combobox.set(c_obj.action)

        core_input_1_label = ctk.CTkLabel(master=core_box,text="Core " + str(c) + ": Input 1")
        core_input_1_combobox = ctk.CTkComboBox(core_box, values=inputs,command=lambda choice, c=c: pld_callback(choice, c, 2))
        core_input_1_combobox.set(c_obj.input_1)

        core_input_2_label = ctk.CTkLabel(master=core_box,text="Core " + str(c) + ": Input 2")
        core_input_2_combobox = ctk.CTkComboBox(core_box, values=inputs,command=lambda choice, c=c: pld_callback(choice, c, 3))
        core_input_2_combobox.set(c_obj.input_2)

        cores.append([core_action_label,core_action_combobox, core_input_1_label, core_input_1_combobox, core_input_2_label, core_input_2_combobox])

    def editing_check():
        if editing.editing == False:
            return
        if editing.past_core_num != editing.core_num:
            for i in range(0,6): cores[editing.core_num][i].pack()
            for i in range(0,6): cores[editing.past_core_num][i].pack_forget()
            editing.past_core_num = editing.core_num
            progress.set(editing.progress_values[editing.core_num])



    def right():
        global editing
        editing.core_num += 1
        if editing.core_num > 5:
            editing.core_num = 0
        editing_check()
        
    def left():
        global editing
        editing.core_num -= 1
        if editing.core_num < 0:
            editing.core_num = 5
        editing_check()
        

    selection_button_frame = ctk.CTkFrame(panel,fg_color="transparent",bg_color="transparent")
    selection_button_frame.pack(pady=5)

    selection_button_frame.grid_columnconfigure((0, 1), weight=1)

    left_button = ctk.CTkButton(selection_button_frame, text="<", width=60, command=left)
    right_button = ctk.CTkButton(selection_button_frame, text=">", width=60, command=right)

    left_button.grid(row=0, column=0, padx=5)
    right_button.grid(row=0, column=1, padx=5)


    for i in range(0,6): cores[editing.core_num][i].pack()

    save_button = ctk.CTkButton(master=panel,text="Save",command=lambda:save(app, panel, program_name.get(), program_name, pld))
    save_button.pack(pady=5)
    
    cancel(panel,5,confirmation=True)


  
    