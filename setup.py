from cx_Freeze import setup, Executable
import sys, re, random, os, math, pygame

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':["sys", "re", "random", "os", "math", "pygame", "idna"],
    },    
}

setup(
    name = "word bomb",
    options = options,
    version = "1",
    description = 'game',
    executables = executables
)

