import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": ["images/", "imageformats/"]}

# GUI applications require a different base on Windows (the default is for a
# console application).

base = None
if sys.platform == "win32":
    exe = Executable(script="semard.py", base="Win32GUI", shortcutName="Semard", shortcutDir="DesktopFolder", icon = "images/animes.ico")
    
else:
    exe = Executable(script="semard.py")

setup(name = "Semard",
        version = "1.0",
        description = "Semard Beta",
        options = {"build_exe": build_exe_options},
        executables = [exe])
