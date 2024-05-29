import sys
from cx_Freeze import setup, Executable

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"

executables = [Executable(
    script="koi-clicker.py",
    base=base,
    icon=r'utils\img\icons\koi.ico'
)]

buildOptions = dict(include_files = ['utils/'])

setup(
    name = "Koi Clicker",
    options = dict(build_exe = buildOptions),
    version = "1.0",
    description = 'Jogo Clicker 2D feito em python',
    executables = executables
)