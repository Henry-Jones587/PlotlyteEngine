# --- imports ---
import subprocess
import random
import threading
import shutil
import os
import sys
import csv
import time

# --- install cryptography if missing ---
try:
    from cryptography.fernet import Fernet
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "cryptography"], check=True)
    from cryptography.fernet import Fernet

# --- DotDot setup ---
from dotdot import *
DotDot.credit = True
DotDot.addstyle("Complete", "\033[0;32m")
DotDot.addstyle("Information", "\033[0;34m")
DotDot.addstyle("Warning", "\033[0;33m\033[1m")
DotDot.addstyle("Error", "\033[0;31m\033[1m")

python_exe = sys.executable

# --- helper functions ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- tips ---
def tip():
    tips = [
       "Tip: Keep your code DRY (Don't Repeat Yourself).",
       "Tip: Write unit tests for your functions.",
       "Tip: Use meaningful variable names.",
       "Tip: Document your code.",
       "Tip: Use version control (like Git) for your projects."
    ]
    DotDot.newprint(random.choice(tips), 0.05, ["Information"])

# --- loading animation ---
def load():
    print("")
    DotDot.load_start()

# --- prepare build environment ---
def prepare_env():
    DotDot.newprint("Preparing build environment...", 0.05, ["Information"])
    try:
        subprocess.run(["pyinstaller", "--version"], check=True)
    except subprocess.CalledProcessError:
        DotDot.newprint("Pyinstaller not found. Installing via pip.", 0.05, ["Warning"])
        subprocess.run([python_exe, "-m", "pip", "install", "pyinstaller"], check=True)
        DotDot.newprint("Dependencies installed successfully.", 0.05, ["Complete"])
    
    try:
        from PIL import Image
    except ImportError:
        DotDot.newprint("Pillow not found. Installing via pip.", 0.05, ["Warning"])
        subprocess.run([python_exe, "-m", "pip", "install", "pillow"], check=True)
        DotDot.newprint("Dependencies installed successfully.", 0.05, ["Complete"])
    
    os.makedirs("build", exist_ok=True)

# --- check current directory files ---
def check_env():
    return [f for f in os.listdir('.') if os.path.isfile(f)]

# --- clear build folder ---
def refresh_build_env():
    os.rmdir('build')

# --- copy files to build folder ---
def change_env(startenv, ignore):
    for file in startenv:
        if file not in ignore:
            shutil.copyfile(f".\\{file}", f".\\build\\{file}")
    # --- copy the assets folder ---
    if os.path.exists("assets"):
        dest_assets = os.path.join("build", "assets")
        if os.path.exists(dest_assets):
            shutil.rmtree(dest_assets)
        shutil.copytree("assets", dest_assets)
    os.chdir("build")


# --- build project using PyInstaller ---
def build_project(Name):
    DotDot.newprint(f"Starting build for {Name}...", 0.05, ["Information"])
    # Add the assets folder to the build
    assets_path = os.path.join(os.getcwd(), "assets")
    add_data = f"{assets_path};assets"  # Windows format

    subprocess.run([
        "pyinstaller",
        f"{Name}.py",
        "--noconfirm",
        "--clean",
        "--add-data", add_data
    ], check=True)
    DotDot.newprint(f"Build completed! Check 'dist/{Name}' for your EXE and assets.", 0.05, ["Complete"])

# --- CSV helper ---
def get_build_info(csv_file, project_name):
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Name'] == project_name:
                    return row['Passwd'], row['Key']
    except FileNotFoundError:
        return None, None
    return None, None

# --- MAIN GUARD ---
if __name__ == "__main__":
    DotDot.newprint("Build tools for Plotlyte...", 0.05)

    # --- get project name ---
    name = input("Enter the name of your project (without .py): ")
    if name.lower().endswith(".py"):
        DotDot.newprint("Notice: You typed the extension '.py'. We'll remove it automatically.", 0.05, ["Warning"])
        name = name[:-3]
    if name == "build":
        DotDot.newprint("That's this file!", 0.05, ["Error"])
        sys.exit()

    csv_file = "build.csv"
    enc_pass, key = get_build_info(csv_file, name)

    # --- handle password check ---
    if enc_pass and key:
        fernet = Fernet(key.encode())
        try:
            correct_pass = fernet.decrypt(enc_pass.encode()).decode()
        except Exception:
            DotDot.newprint("Error decrypting password. The build key may be corrupted.", 0.05, ["Error"])
            sys.exit()
        user_pass = InputPro("Please enter the project build password: ", Style=["Warning"]).Mask()
        if user_pass != correct_pass:
            DotDot.newprint("Incorrect password.", 0.05, ["Error"])
            sys.exit()
    else:
        DotDot.newprint("No previous build found. Creating new build credentials.", 0.05, ["Information"])
        key = Fernet.generate_key().decode()
        fernet = Fernet(key.encode())
        new_pass = InputPro("Set a build password for this project (save it safely!): ", Style=["Warning"]).Mask()
        enc_pass = fernet.encrypt(new_pass.encode()).decode()
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat(csv_file).st_size == 0:
                writer.writerow(['Name', 'Passwd', 'Key'])
            writer.writerow([name, enc_pass, key])
        DotDot.newprint("IMPORTANT: Save your build password securely!", 0.05, ["Warning"])

    ignore = ["eldoria.json", "main.py", "game_schema.json", "build.py", "build.csv"]

    # --- prepare, refresh, and change env ---
    refresh_build_env()
    prepare_env()
    env = check_env()
    change_env(env, ignore)

    # --- loading + tips ---
    time.sleep(0.5)
    for _ in range(3):  # show 3 tips
        subprocess.run("cls", shell=True)
        tip()
        time.sleep(3)
    subprocess.run("cls", shell=True)

    loading = threading.Thread(target=load)
    loading.start()

    # --- build project ---
    build_project(name)
    DotDot.loading = False
