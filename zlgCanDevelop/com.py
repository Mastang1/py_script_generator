from pickletools import bytes1
from zlgcan import *
import cantools
from can.io import BLFReader

DEVICE_LIST = [
ZCAN_PCI5121              ,
ZCAN_PCI9810              ,
ZCAN_USBCAN1              ,
ZCAN_USBCAN2              ,
ZCAN_PCI9820              ,
ZCAN_CAN232               ,
ZCAN_PCI5110              ,
ZCAN_CANLITE              ,
ZCAN_ISA9620              ,
ZCAN_ISA5420              ,
ZCAN_PC104CAN             ,
ZCAN_CANETUDP             ,
ZCAN_CANETE               ,
ZCAN_DNP9810              ,
ZCAN_PCI9840              ,
ZCAN_PC104CAN2            ,
ZCAN_PCI9820I             ,
ZCAN_CANETTCP             ,
ZCAN_PCIE_9220            ,
ZCAN_PCI5010U             ,
ZCAN_USBCAN_E_U           ,
ZCAN_USBCAN_2E_U          ,
ZCAN_PCI5020U             ,
ZCAN_EG20T_CAN            ,
ZCAN_PCIE9221             ,
ZCAN_WIFICAN_TCP          ,
ZCAN_WIFICAN_UDP          ,
ZCAN_PCIe9120             ,
ZCAN_PCIe9110             ,
ZCAN_PCIe9140             ,
ZCAN_USBCAN_4E_U          ,
ZCAN_CANDTU_200UR         ,
ZCAN_CANDTU_MINI          ,
ZCAN_USBCAN_8E_U          ,
ZCAN_CANREPLAY            ,
ZCAN_CANDTU_NET           ,
ZCAN_CANDTU_100UR         ,
ZCAN_PCIE_CANFD_100U      ,
ZCAN_PCIE_CANFD_200U      ,
ZCAN_PCIE_CANFD_400U      ,
ZCAN_USBCANFD_200U        ,
ZCAN_USBCANFD_100U        ,
ZCAN_USBCANFD_MINI        ,
ZCAN_CANFDCOM_100IE       ,
ZCAN_CANSCOPE             ,
ZCAN_CLOUD                ,
ZCAN_CANDTU_NET_400       ,
ZCAN_CANFDNET_TCP         ,
ZCAN_CANFDNET_200U_TCP    ,
ZCAN_CANFDNET_UDP         ,
ZCAN_CANFDNET_200U_UDP    ,
ZCAN_CANFDWIFI_TCP        ,
ZCAN_CANFDWIFI_100U_TCP   ,
ZCAN_CANFDWIFI_UDP        ,
ZCAN_CANFDWIFI_100U_UDP   ,
ZCAN_CANFDNET_400U_TCP    ,
ZCAN_CANFDNET_400U_UDP    ,
ZCAN_CANFDBLUE_200U       ,
ZCAN_CANFDNET_100U_TCP    ,
ZCAN_CANFDNET_100U_UDP    ,
ZCAN_CANFDNET_800U_TCP    ,
ZCAN_CANFDNET_800U_UDP    ,
ZCAN_USBCANFD_800U        ,
ZCAN_PCIE_CANFD_100U_EX   ,
ZCAN_PCIE_CANFD_400U_EX   ,
ZCAN_PCIE_CANFD_200U_MINI ,
ZCAN_PCIE_CANFD_200U_M2   ,
ZCAN_CANFDDTU_400_TCP     ,
ZCAN_CANFDDTU_400_UDP     ,
ZCAN_CANFDWIFI_200U_TCP   ,
ZCAN_CANFDWIFI_200U_UDP   ,
ZCAN_CANFDDTU_800ER_TCP   ,
ZCAN_CANFDDTU_800ER_UDP   ,
ZCAN_CANFDDTU_800EWGR_TCP ,
ZCAN_CANFDDTU_800EWGR_UDP ,
ZCAN_CANFDDTU_600EWGR_TCP ,
ZCAN_CANFDDTU_600EWGR_UDP ,
ZCAN_CANFDDTU_CASCADE_TCP ,
ZCAN_CANFDDTU_CASCADE_UDP ,
ZCAN_USBCANFD_400U        ,
ZCAN_CANFDDTU_200U        ,
ZCAN_ZPSCANFD_TCP         ,
ZCAN_ZPSCANFD_USB         ,
ZCAN_CANFDBRIDGE_PLUS 
]


class COM:
    BLFMsgs = []
    db = cantools.db.Database
    zcanlib = ZCAN()

    def __init__(self):
        pass

    def LoadBLF(self, filename):
        self.BLFMsgs = BLFReader(filename)
        print("BLF file loaded")
        return
        # alternative
        log = BLFReader(filename)
        for msg in log:
            self.BLFMsgs.append(msg)
            break

    def LoadDBC(self, filename):
        self.db = cantools.db.load_file(filename)

    def PrintBLF(self):
        for message in self.BLFMsgs:
            print(
                f"Tstamp: {message.timestamp}",
                f"\tID: {message.arbitration_id}",
                f"\tExtended: {message.is_extended_id}",
                f"\tRemote Frame: {message.is_remote_frame}",
                f"\tRX: {message.is_rx}",
                f"\tDLC: {message.dlc}",
                f" \tData: {'x'.join([f'{b:02X}' for b in message.data])}",
                f"\tChannel: {message.channel}",
            )

    def OpenUsbCanII(self):
        dhandle = self.zcanlib.OpenDevice(ZCAN_USBCAN2, 0, 0)
        if dhandle == INVALID_DEVICE_HANDLE:
            print("failed to open device")
            exit(0)
        print("device handle: " + dhandle)
        return dhandle

    def OpenUsbCanOnBus(self, bus):
        dhandle = self.zcanlib.OpenDevice(bus, 0, 0)
        if dhandle == INVALID_DEVICE_HANDLE:
            print("bus open failed: " + str(bus))
            return INVALID_DEVICE_HANDLE
        print("opened device handle: " + str(hex(dhandle)))
        return dhandle

    def SearchAllBuses(self):
        for i in DEVICE_LIST:
            if i != ZCAN_CANSCOPE and i != ZCAN_CLOUD:
                self.OpenUsbCanOnBus(i)

    def OpenChannel(self, dev_handle, channel):


        chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
        chn_init_cfg.can_type = ZCAN_TYPE_CAN
        chn_init_cfg.config.can.acc_mode = 0
        chn_init_cfg.config.can.acc_mask = 0xFFFFFFFF
        chn_init_cfg.config.can.timing0 = 0
        chn_init_cfg.config.can.timing1 = 28
        chn_handle = self.zcanlib.InitCAN(dev_handle, channel, chn_init_cfg)
        if chn_handle is None:
            print("Channel handle is none.")
            return None
        self.zcanlib.StartCAN(chn_handle)
        return chn_handle


    def OpenChannelByDefaultParam(self, device_handle, chn):
        ip = self.zcanlib.GetIProperty(device_handle)
        ret = self.zcanlib.SetValue(ip, str(chn) + "/canfd_standard", "0")
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d CANFD standard failed!" %(chn))
            exit(0)
        ret = self.zcanlib.SetValue(ip, str(chn) + "/initenal_resistance", "1")
        if ret != ZCAN_STATUS_OK:
            print("Open CH%d resistance failed!" %(chn))
            exit(0)
        ret = self.zcanlib.SetValue(ip,str(chn)+"/canfd_abit_baud_rate","500000")  #设置波特率
        ret = self.zcanlib.SetValue(ip,str(chn)+"/canfd_dbit_baud_rate","2000000")
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d baud failed!" %(chn))      
            exit(0)
            
        ret = self.zcanlib.SetValue(ip, "0/set_cn","A001")
        if ret == ZCAN_STATUS_OK:
            t = self.zcanlib.GetValue(ip, "0/get_cn/1")
            print(type(t)) 
            print(str(t))   
            

        chn_init_cfg = ZCAN_CHANNEL_INIT_CONFIG()
        chn_init_cfg.can_type = ZCAN_TYPE_CANFD
        chn_init_cfg.config.canfd.mode  = 0
        chn_handle = self.zcanlib.InitCAN(device_handle, chn, chn_init_cfg)
        if chn_handle ==0:
            print("initCAN failed!" %(chn))  
            exit(0)
    ###SET filter  
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_clear","0")
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_clear failed!" %(chn))
            exit(0)
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_mode","0")    #标准帧滤波
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_mode failed!" %(chn)) 
            exit(0)
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_start","0")    
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_start failed!" %(chn))  
            exit(0)        
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_end","0x7FF")    
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_end failed!" %(chn)) 
            exit(0)
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_mode","1")    #扩展帧滤波
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_mode failed!" %(chn))
            exit(0)
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_start","0")    
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_start failed!" %(chn))
            exit(0)        
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_end","0x1FFFFFFF")    
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_end failed!" %(chn))
            exit(0)
        ret = self.zcanlib.SetValue(ip,str(chn)+"/filter_ack","0")    
        if ret != ZCAN_STATUS_OK:
            print("Set CH%d  filter_ack failed!" %(chn))
            exit(0)

        ret=self.zcanlib.StartCAN(chn_handle)
        if ret != ZCAN_STATUS_OK:
            print("startCAN failed!" %(chn))
            exit(0)  



    def TransmitCan(self, chn_handle, stdorext, id, data, len):
        transmit_num = 1
        msgs = (ZCAN_Transmit_Data * transmit_num)()
        for i in range(transmit_num):
            msgs[i].transmit_type = 0
            msgs[i].frame.eff = 0
            if stdorext:
                msgs[i].frame.eff = 1
            msgs[i].frame.rtr = 0
            msgs[i].frame.can_id = id
            msgs[i].frame.can_dlc = len
            for j in range(msgs[i].frame.can_dlc):
                msgs[i].frame.data[j] = data[j]
        ret = self.zcanlib.Transmit(chn_handle, msgs, transmit_num)
        print('Trans bytes is :', ret)

    def ReceiveAndPrintCan(self, chn_handle):
        rcv_num = self.zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
        if rcv_num:
            print("Receive CAN message number: %d" % rcv_num)
            rcv_msg, rcv_num = self.zcanlib.Receive(chn_handle, rcv_num)
            for i in range(rcv_num):
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

    class Message:
        def __init__(self, frame_data):
            self.frame = COM.Frame(frame_data)

    class Frame:
        def __init__(self, data):
            self.data = data

    def ReceiveCan(self, chn_handle):
        rcv_num = self.zcanlib.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
        # TODO: just for testing
        rcv_msg = [COM.Message([0xF0, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7])]
        return rcv_msg, rcv_num
        if rcv_num:
            rcv_msg, rcv_num = self.zcanlib.Receive(chn_handle, rcv_num)
        return rcv_msg, rcv_num
