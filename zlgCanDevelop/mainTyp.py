import platform
import sys, time
import os
import threading
from com import COM, DEVICE_LIST
from zlgcan import *
# if __name__ == "__main__":
#     if platform.python_version() >= "3.8.0":
#         os.add_dll_directory(os.getcwd())
#     #ZCAN_VIRTUAL_DEVICE
#     myCan = Tester(ZCAN_USBCANFD_400U, 3)
#     myCan.SampleSendReceive()
#     time.sleep(5)
#     myCan.End()

def input_thread():
   input()

if __name__ == "__main__":
    #ZCAN_VIRTUAL_DEVICE
    devUSBCANFD400 = COM()
    deviceHandle = devUSBCANFD400.OpenUsbCanOnBus(ZCAN_VIRTUAL_DEVICE)
    info = devUSBCANFD400.zcanlib.GetDeviceInf(deviceHandle)
    print("Device Information:\n%s" %(info))
    canChn0 = devUSBCANFD400.OpenChannel(deviceHandle, 0)
    canChn1 = devUSBCANFD400.OpenChannel(deviceHandle, 1)
    print("handle1:", canChn0, "handle2:", canChn1)

    # thread_quit=threading.Thread(target=input_thread)
    # thread_quit.start()   

    loopTimes = 20
    while True:
        # com_1.ReceiveAndPrintCan(0)
        time.sleep(0.5)
        print(" com1...")
        loopTimes -=1


    


