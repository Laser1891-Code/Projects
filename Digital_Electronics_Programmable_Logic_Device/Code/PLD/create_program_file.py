import os

def create_program(app):
    os.chdir(app.save_dir)
    filename = "New Program"
    base_name = filename
    count = 1
    while os.path.exists(filename):
        filename = f"{base_name} ({count})"
        count += 1

    with open(filename, "w") as f:
        f.write("000-000-00|000-000-00|000-000-00|000-000-00|000-000-00|000-000-00")
    
    app.program = filename
    
    if app.program != "No Program Selected":     
        from main_program_file import set_program_panel
        set_program_panel(app)



