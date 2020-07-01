"""2.Interface for running exocross
For now it will be identical to what was created for DuoDataGenerator - https://github.com/MorsePotential/DuoDataGenerator/blob/master/duoXInterface.py
@todo: come up with a better way of calling an exectuable
@body: add a better way of handling executables rather than calling file from console
"""
import os
import sys
import subprocess 

jobpath=os.getcwd()


def launchExoCrosswithOutputfileSpecified(inFileName, outFileName,exoCross):
    """
    @todo: add mac version
    """
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        command="./{}.exe <{}> {}".format(exoCross,inFileName,outFileName)
        os.system(command)
    elif sys.platform.startswith("win32"):
        command="{}.exe <{}> {}".format(exoCross,inFileName,outFileName)
        os.system(command)
    else:
        print("Unsupported version of OS")
    pass

def launchExocrossOnlyInput(inFileName, exoCross):
    """
    @todo: add mac version
    """
    try:
        os.environ.pop('PYTHONIOENCODING')
    except KeyError:
        pass
    
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        command="./{}.exe <{}".format(exoCross,inFileName)
        os.system(command)
    elif sys.platform.startswith("win32"):
        command="{}.exe <{}".format(exoCross,inFileName)
        subprocess.Popen(command,cwd=jobpath,)
    else:
        print("Unsupported version of OS")
    pass

def remove(inFileName):
    os.remove(inFileName)
    pass

def prepEnvironment():
    """
    @todo: add mac version
    """
    if sys.platform.startswith("win32"):
        command="run_exocross.bat"
        os.system(command)
    pass
