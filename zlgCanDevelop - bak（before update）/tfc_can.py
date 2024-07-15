###
import time
import random

from zlgcan import *
from com import COM, DEVICE_LIST


class can(COM): #Basic class DevIf
    dev_handle = INVALID_DEVICE_HANDLE
    chn_handle = INVALID_CHANNEL_HANDLE
    packetsLog = {}

    def __init__(self, bus, channel=0, configInfo = '') -> None:
        self.dev_handle = super().OpenUsbCanOnBus(bus)
        if self.dev_handle == INVALID_DEVICE_HANDLE:
            return
        self.__Config()
        

    def Open():
        self.chn_handle = super().OpenChannel(self.dev_handle, channel)

    def Close():
        super().zcanlib.ResetCAN(self.chn_handle)
        super().zcanlib.CloseDevice(self.dev_handle)
        print("Finish")

    def __Config(configInfo = ''):
        #Change baudrate etc.
        pass

    def Read():
        pass

    def Write():
        pass






    def SampleSendReceive(self):
        data = [0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7]
        super().TransmitCan(self.chn_handle, 0, 0x100, data, 8)
        # super().TransmitCan(self.chn_handle, 1, 0x12345678, data, 8)

        time.sleep(0.1)
        super().zcanlib.ClearBuffer(self.chn_handle)
        time.sleep(0.1)
        super().ReceiveAndPrintCan(self.chn_handle)

    def SendCanFromBLC(self, interval=0.1):
        for msg in self.BLFMsgs:
            super().TransmitCan(
                chn_handle=self.chn_handle,
                stdorext=msg.is_extended_id,
                id=msg.arbitration_id,
                data=msg.data,
                len=msg.dlc,
            )
            time.sleep(interval)