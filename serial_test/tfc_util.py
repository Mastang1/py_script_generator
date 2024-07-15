import time, os, sys, serial

class tfcUtil:
    def __init__(self) -> None:
        pass

    def tfcOpen(self, com, rate = 115200, timeout = 10):
        self.cmdCom = serial.Serial(com, baudrate=rate, timeout=timeout)

    def tfcClose(self):
        self.cmdCom.close()

    def tfcSendCmd(self, Command):
        Command = Command + '\r\n'
        byteSend = self.cmdCom.write(Command.encode())

    def tfcReadResponse(self):
        reponseStr = self.cmdCom.readline().decode()
        print(reponseStr)
        return reponseStr
    
    def tfcSyncSession(self, Command):
        responseList = ''
        responseStr = ''
        self.tfcSendCmd(Command)
        while "OK" not in responseStr:
            responseStr = self.tfcReadResponse()
            responseList = responseList + responseStr
            time.sleep(100/1000)

        return responseList

