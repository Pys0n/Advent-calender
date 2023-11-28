from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *

screensize = (1376,846)

def getPath(path: str):
    path = str(Path.cwd())+'/'+path
    #return path.replace('/', '\\') # windows
    return path                     # linux

def getFullPath(path: str):
    path = str(Path.cwd())+'/'+path
    return path.replace('\\', '/')