###
import time, os, sys
import random
import threading

from zlgcan import *
from com import COM, DEVICE_LIST


class TfcZlgCan(): #Basic class DevIf
    __gZCan = None
    __gDevHandle = INVALID_DEVICE_HANDLE

    def __init__(self, canDevType = ZCAN_USBCANFD_400U ):
        self.tfcCanChan = None
        if TfcZlgCan.__gZCan == None:
            TfcZlgCan.__gZCan = ZCAN()

        if TfcZlgCan.__gDevHandle == INVALID_DEVICE_HANDLE:
            TfcZlgCan.__gDevHandle = TfcZlgCan.__gZCan.OpenDevice(canDevType, 0, 0)
            info = TfcZlgCan.__gZCan.GetDeviceInf(TfcZlgCan.__gDevHandle)
            print("Device Information:\n%s" %(info))
        else:
            print("Current deviece is Exist.")

    # 
    def Open(self, canChan = 0, can_type = ZCAN_TYPE_CAN):
        if TfcZlgCan.__gDevHandle == INVALID_DEVICE_HANDLE:
            print('Device open error.')
            return None
        
        chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
        chn_init_cfg.can_type = can_type
        if can_type == 'can':
            chn_init_cfg.config.can.acc_mode = 0
            chn_init_cfg.config.can.acc_mask = 0xFFFFFFFF
            chn_init_cfg.config.can.filter = 1
            # 3 transmit only once 2. trasmit to self  1. just listen
            chn_init_cfg.config.can.mode = 0
            # chn_init_cfg.config.can.pad = 0 

        else:
            chn_init_cfg.config.canfd.acc_mode = 0
            chn_init_cfg.config.canfd.acc_mask = 0xFFFFFFFF
            chn_init_cfg.config.canfd.brp = 0
            chn_init_cfg.config.canfd.filter = 1
            chn_init_cfg.config.canfd.mode = 0
            # chn_init_cfg.config.canfd.pad = 0 

        self.tfcCanChan = TfcZlgCan.__gZCan.InitCAN(TfcZlgCan.__gDevHandle, canChan, chn_init_cfg)

        if self.tfcCanChan is INVALID_CHANNEL_HANDLE:
            print("Channel handle is none.")
            return None
        if ZCAN_STATUS_OK != self.__gZCan.StartCAN(self.tfcCanChan):
            print(" CAN Open failed.")
            return None
        print(" CAN Open.")

        return self.tfcCanChan


    '''
    TODO: add canfd 
    rcv_can_msgs = (ZCAN_Receive_Data * rcv_num)()
    '''
    def Read(self, can_type = ZCAN_TYPE_CAN):
        self.rcv_num = TfcZlgCan.__gZCan.GetReceiveNum(self.tfcCanChan, can_type)
        if self.rcv_num:
            print("Receive CAN message number: %d" % self.rcv_num)
            self.rcv_msg, self.rcv_actural = TfcZlgCan.__gZCan.Receive(self.tfcCanChan, rcv_num = self.rcv_num)
            print(" Received data number is :", self.rcv_actural, "Type is :", type(self.rcv_msg))

            for i in range(self.rcv_actural):
                print(
                    "[%d]:ts:%d, id:0x%x, dlc:%d, eff:%d, rtr:%d, data:%s"
                    % (
                        i,
                        rcv_msg[i],
                        rcv_msg[i].timestamp,
                        rcv_msg[i].frame.can_id,
                        rcv_msg[i].frame.dlc,
                        rcv_msg[i].frame.eff,
                        rcv_msg[i].frame.rtr,
                        "".join(
                            hex(
                                rcv_msg[i].frame.data[j][2:] + " "
                                for j in range(rcv_msg[i].frame.can_dlc)
                            )
                        ),
                    )
                )
        

    def Write(self, stdorext, id, data, len):
        self.msg = (ZCAN_Transmit_Data)()
        self.msg.transmit_type = 0

        self.msg.frame.eff = 0
        if stdorext:
            self.msg.frame.eff = 1
        self.msg.frame.rtr = 0
        self.msg.frame.can_id = id
        self.msg.frame.can_dlc = len

        for j in range(self.msg.frame.can_dlc):
            self.msg.frame.data[j] = data[j]

        self.ret = TfcZlgCan.__gZCan.Transmit(self.tfcCanChan, self.msg, 1)
        print('Trans frame is :', self.ret)

    def Close(self):
        TfcZlgCan.__gZCan.ResetCAN(self.tfcCanChan)
        print("Finish")

    def ClsoseDev(self):
        TfcZlgCan.__gZCan.ResetCAN(self.tfcCanChan)
        TfcZlgCan.__gZCan.CloseDevice(TfcZlgCan.__gDevHandle)
        print("Close device.")








def taskCAN0Trans(canChanHandle):
    
    canChanHandle.Open(canChan = 0)

    myData = [1,2,3,4,5,6,7,8]
    while True:
        canChanHandle.Write(0, 100, myData, 8)
        time.sleep(2)
        if not threading.main_thread().is_alive():
            break

def input_thread():
   input()



def start_test(zcanlib, device_handle, chn): 
    ip = zcanlib.GetIProperty(device_handle)
    ret = zcanlib.SetValue(ip,str(chn)+"/baud_rate","500000")
    ret = zcanlib.SetValue(ip,str(chn)+"/protocol","0")
    chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
    chn_init_cfg.can_type = ZCAN_TYPE_CAN
    chn_init_cfg.config.canfd.mode  = 0
    chn_handle = zcanlib.InitCAN(device_handle, chn, chn_init_cfg)
    if chn_handle ==0:
        print("initCAN failed!" %(chn))  
        exit(0)

    ret=zcanlib.StartCAN(chn_handle)
    if ret != ZCAN_STATUS_OK:
        print("startCAN failed!" %(chn))
        exit(0)  

    zcanlib.ReleaseIProperty(ip) 
    return chn_handle


def test_can_rcv(zcanlib, chn_handle):
    if chn_handle is INVALID_CHANNEL_HANDLE:
        print(" -- ERROR ", __name__)

    while True:
        time.sleep(1)
        rcv_num = zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
        my_error = zcanlib.ReadChannelErrInfo(chn_handle)
        print(" Error code is :", my_error.error_code, "and the Channel handle is :", chn_handle)

        if rcv_num:
            print("Receive CAN message number:%d" % rcv_num)
            rcv_msg, rcv_num = zcanlib.Receive(chn_handle, rcv_num, wait_time = -1)
            print(" Received data number is :", rcv_num, "Type is :", type(rcv_msg))
            for i in range(2):
                print("[%d]:timestamps:%d,type:CAN, id:%s, dlc:%d, eff:%d, rtr:%d, data:%s" %(i, rcv_msg[i].timestamp, 
                      hex(rcv_msg[i].frame.can_id), rcv_msg[i].frame.can_dlc, 
                      rcv_msg[i].frame.eff, rcv_msg[i].frame.rtr,
                      ''.join(hex(rcv_msg[i].frame.data[j])+ ' 'for j in range(8))))
        
        # if not threading.main_thread().is_alive():
        #     break

 
if __name__ == "__main__":
    zcanlib = ZCAN() 
    testcantype =0 #0:CAN; 1:canfd
    handle = zcanlib.OpenDevice(ZCAN_VIRTUAL_DEVICE, 0,0)
    if handle == INVALID_DEVICE_HANDLE:
        print("Open CANFD Device failed!")
        exit(0)
    print("device handle:%d." %(handle))

    info = zcanlib.GetDeviceInf(handle)
    print("Device Information:\n%s" %(info))

    #Start CAN
    chn_handle_rcv = start_test(zcanlib, handle, 0)
    chn_handle_tx = start_test(zcanlib, handle, 1)
    print("channel handle:%d." %(chn_handle_rcv))
    print("channel handle:%d." %(chn_handle_tx))

    thread_cmd=threading.Thread(target=input_thread)
    thread_cmd.start()

    thread=threading.Thread(target=test_can_rcv, args=(zcanlib, chn_handle_rcv, ))
    thread.start()
    #Send CAN Messages
    transmit_num = 5
    msgs = (ZCAN_Transmit_Data * transmit_num)()

    while True:
        for i in range(transmit_num):
            msgs[i].transmit_type = 0 #0-正常发送，2-自发自收
            msgs[i].frame.eff     = 0 #0-标准帧，1-扩展帧
            msgs[i].frame.rtr     = 0 #0-数据帧，1-远程帧
            msgs[i].frame.can_id  = i
            msgs[i].frame.can_dlc = 8
            for j in range(msgs[i].frame.can_dlc):
                msgs[i].frame.data[j] = j
        ret = zcanlib.Transmit(chn_handle_tx, msgs, transmit_num)
        print("transmit Num: %d." % ret)
        sys.stdout.buffer.write(msgs)
        time.sleep(5)
        if not thread_cmd.is_alive():
            break

    #Close CAN 
    ret=zcanlib.ResetCAN(chn_handle_tx)
    ret=zcanlib.ResetCAN(chn_handle_rcv)
    if ret==1:
        print("ResetCAN success! ")
    #Close Device
    ret=zcanlib.CloseDevice(handle)
    if ret==1:
        print("CloseDevice success! ")

