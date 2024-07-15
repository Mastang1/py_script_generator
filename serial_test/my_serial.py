import time, serial, os, sys
from tfc_util import tfcUtil

myCom = tfcUtil()
myCom.tfcOpen("COM1")
print(myCom.tfcSyncSession("hello"))
myCom.tfcClose()