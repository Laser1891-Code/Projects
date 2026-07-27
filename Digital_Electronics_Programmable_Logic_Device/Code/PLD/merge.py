import subprocess
import sys
import os
import json
import time

# Get resource path (works with PyInstaller)
def resource(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.getcwd(), path)

CLI = resource("arduino-cli.exe")
CONFIG = resource("arduino-cli.yaml")
SKETCH = resource("sketch")

FQBN = "adafruit:samd:adafruit_itsybitsy_m4"

# Auto-detect COM port by VID
def find_com_port():
    cmd = [
        CLI,
        "--config-file", CONFIG,
        "board", "list",
        "--format", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    for entry in data.get("detected_ports", []):
        port = entry.get("port", {})
        props = port.get("properties", {})
        vid = props.get("vid", "").lower()

        if vid == "0x239a":
            return port.get("address")

    # Fallback: return first port if VID not found
    if data.get("detected_ports"):
        return data["detected_ports"][0]["port"]["address"]

    raise RuntimeError("Adafruit board not found")

# Reset SAMD board into bootloader using 1200 bps trick
def reset_board(port):
    try:
        import serial
    except ImportError:
        print("Warning: PySerial not installed. Skipping auto-reset.")
        return

    try:
        ser = serial.Serial(port, 1200)
        ser.close()
        time.sleep(4)  # give bootloader time to enumerate
    except Exception as e:
        print(f"Error resetting board: {e}")

# Find bootloader COM port
def find_bootloader_port(original_port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        cmd = [
            CLI,
            "--config-file", CONFIG,
            "board", "list",
            "--format", "json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        for entry in data.get("detected_ports", []):
            port = entry.get("port", {})
            addr = port.get("address")
            if addr != original_port:
                props = port.get("properties", {})
                vid = props.get("vid", "").lower()
                if vid == "0x239a" or not vid:
                    return addr
        time.sleep(0.5)

    raise RuntimeError("Bootloader port not found")

def upload():
    port = find_com_port()
    print(f"Detected board on {port}")

    print("Resetting board into bootloader...")
    reset_board(port)

    print("Waiting for bootloader port...")
    boot_port = find_bootloader_port(port)
    print(f"Bootloader port detected: {boot_port}")

    print("Uploading sketch...")
    cmd = [
        CLI,
        "--config-file", CONFIG,
        "compile",
        "--upload",
        "-p", boot_port,
        "--fqbn", FQBN,
        SKETCH
    ]

    try:
        # Capture stdout and stderr
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        print("Upload complete!")
    except subprocess.CalledProcessError as e:
        print("Arduino CLI failed!")
        print("Return code:", e.returncode)
        print("==== STDOUT ====")
        print(e.stdout)
        print("==== STDERR ====")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    upload()
