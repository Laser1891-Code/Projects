import subprocess
import sys
import os
import json
import time
from messagebox_file import messagebox
from error_file import error

# -------------------------
# Resource helper
# -------------------------

cont = True

def resource(file):
    if hasattr(sys, "_MEIPASS"):
        path = os.path.join(sys._MEIPASS, file)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, file)
    abs_path = os.path.abspath(path)
    return abs_path

def setup_sketch_dir(save_dir):
    sketches = os.path.join(save_dir, "sketches")
    sketch = os.path.join(sketches, "PLD")
    os.makedirs(sketch, exist_ok=True)
    return sketch


CLI = resource("arduino-cli.exe")
CONFIG = resource("arduino-cli.yaml")
SKETCH = None

# ItsyBitsy 32u4
FQBN = "adafruit:avr:itsybitsy32u4_3V"

# -------------------------
# Ensure Arduino15 folder exists in Saved Programs
# -------------------------
def setup_arduino15(save_dir):
    bundled_arduino15 = os.path.join(save_dir, "Arduino15")
    os.makedirs(bundled_arduino15, exist_ok=True)
    os.environ["ARDUINO_DATA_DIR"] = bundled_arduino15
    return bundled_arduino15

# -------------------------
# Ensure core is installed
# -------------------------
def ensure_core(ARDUINO15):
    os.environ["ARDUINO_DATA_DIR"] = ARDUINO15

    # List cores
    result = subprocess.run([CLI, "--config-file", CONFIG, "core", "list"],
                            capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    # Install arduino:avr if missing
    if "arduino:avr" not in result.stdout:
        print("Arduino AVR core missing, installing...")
        subprocess.run([CLI, "--config-file", CONFIG, "core", "update-index"], check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run([CLI, "--config-file", CONFIG, "core", "install", "arduino:avr"], check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        print("Arduino AVR core installed.")

    # Install adafruit:avr if missing
    if "adafruit:avr" not in result.stdout:
        print("Adafruit AVR core missing, installing...")
        subprocess.run([CLI, "--config-file", CONFIG, "core", "install", "adafruit:avr"], check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        print("Adafruit AVR core installed.")

# -------------------------
# Find COM port
# -------------------------
def find_com_port():
    global cont
    cmd = [CLI, "--config-file", CONFIG, "board", "list", "--format", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True,creationflags=subprocess.CREATE_NO_WINDOW)

    data = json.loads(result.stdout)

    for entry in data.get("detected_ports", []):
        props = entry.get("port", {}).get("properties", {})
        vid = props.get("vid", "").lower()
        if vid in ("0x239a", "0x03eb"):
            port = entry["port"]["address"]
            return port

    if data.get("detected_ports"):
        port = data["detected_ports"][0]["port"]["address"]
        return port

    print("No ItsyBitsy detected.")
    cont = False
    return False
# -------------------------
# Compile + Upload
# -------------------------
def upload(app, progress_bar):
    global cont
    progress_bar.set(0)
    app.update_idletasks()

    # Setup Arduino15 in saved dir
    ARDUINO15 = setup_arduino15(app.save_dir)
    SKETCH = setup_sketch_dir(app.save_dir)
    ensure_core(ARDUINO15)

    # -------------------------
    # Compile
    # -------------------------
    if cont:
        compile_cmd = [CLI, "--config-file", CONFIG, "compile", "--fqbn", FQBN, SKETCH]
        try:
            result = subprocess.run(compile_cmd, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Compile Success")
            progress_bar.set(0.25)
            app.update_idletasks()

        except subprocess.CalledProcessError as e:
            print(f"[DEBUG] Compile Failed! Return code: {e.returncode}")
            print(f"[DEBUG] Compile stdout:\n{e.stdout}")
            print(f"[DEBUG] Compile stderr:\n{e.stderr}")
            error(app,"Code upload failed.")
            progress_bar.set(1)
            return
        # -------------------------
        # Wait for board
        # -------------------------
        print("Waiting for board...")
        time.sleep(2)
        progress_bar.set(0.5)
        app.update_idletasks()
        
        port = find_com_port()
        if not port:
            error(app,"Cable not connected. Please try again.")
            progress_bar.set(1)
            return
        print(f"Uploading to {port}")

        # -------------------------
        # Upload
        # -------------------------
        upload_cmd = [CLI, "--config-file", CONFIG, "upload", "-p", port, "--fqbn", FQBN, SKETCH]
        try:
            result = subprocess.run(upload_cmd, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Upload Success")
            progress_bar.set(1)
            app.update_idletasks()
            messagebox(app,"Success!","The code was successfully updated.","Continue",None)

        except subprocess.CalledProcessError as e:
            print(f"[DEBUG] Upload Failed! Return code: {e.returncode}")
            error(app,"Code upload failed.")
            progress_bar.set(1)
            print(f"[DEBUG] Upload stdout:\n{e.stdout}")
            print(f"[DEBUG] Upload stderr:\n{e.stderr}")
            return

        print("Done.")
    else:
        error(app,"Code upload failed.")
        progress_bar.set(1)


# -------------------------
# App container
# -------------------------
class app_class():
    save_dir = ""

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    app = app_class()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    SAVE_DIR = os.path.join(script_dir, "Saved Programs")
    app.save_dir = SAVE_DIR
    upload(app)
