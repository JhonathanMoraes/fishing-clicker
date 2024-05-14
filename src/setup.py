import sys
from cx_Freeze import setup, Executable

executables = [Executable(
    script="clicker.py",
    base=None,
    icon=r'utils\img\fish.ico'
)]

buildOptions = dict(include_files = ['utils/'])

setup(
    name = "Fishing Clicker",
    options = dict(build_exe = buildOptions),
    version = "1.0",
    description = 'Jogo 2D feito em python',
    executables = executables
)