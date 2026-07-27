import re
import os

INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1F]'
WINDOWS_RESERVED = {
    "CON","PRN","AUX","NUL",
    *{f"COM{i}" for i in range(1,10)},
    *{f"LPT{i}" for i in range(1,10)},
}

def safe_filename(app, name, default="",overwrite=False):
    name = re.sub(INVALID_CHARS, "", name)     # Remove illegal chars
    name = name.strip(" .")                     # Ensure no trailing dots/spaces

    if not name:
        name = default

    base, ext = os.path.splitext(name)

    if base.upper() in WINDOWS_RESERVED:
        base = f"_{base}"

    filename = base + ext
    os.chdir(app.save_dir)
    if not overwrite:

        base_name = filename
        count = 1
        while os.path.exists(filename):
            filename = f"{base_name} ({count})"
            count += 1

    return filename
