import cx_Freeze
import sys

NOME_ARQUIVO_JOGO = "main.py" # Exemplo: 'meu_jogo.py', 'game.py', etc.

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "packages": [
        "pygame",
        "random",
        "os",
        "math",
        "tkinter",          
        "speech_recognition", 
        "pyttsx3",          
        "json"              
    ],
    "include_files": [
        "assets/",          
        "recursos/",        
        "base.atitus"      
    ],
    "excludes": ["PyQt5", "PyQt6", "PySide2", "PySide6", "numpy", "scipy", "matplotlib", "test", "unittest"],
    "build_exe": "build/LightningMcQueen_Executavel"
}

executables = [
    cx_Freeze.Executable(
        script=NOME_ARQUIVO_JOGO,
        base=base, 
        icon="assets/icone.ico" 
    )
]

cx_Freeze.setup(
    name="Lightning McQueen",
    version="1.0", 
    description="Um jogo divertido com Lightning McQueen!",
    options={"build_exe": build_exe_options},
    executables=executables
)