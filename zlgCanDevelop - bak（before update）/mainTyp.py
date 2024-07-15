import platform
import sys
import os
from tester import *

if __name__ == "__main__":
    if platform.python_version() >= "3.8.0":
        os.add_dll_directory(os.getcwd())
    #ZCAN_VIRTUAL_DEVICE
    myCan = Tester(ZCAN_VIRTUAL_DEVICE)
    myCan.SampleSendReceive()

    


