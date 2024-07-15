import string, os, sys
from tfcParamMang import ParamsOneCase


class TcGenerator:
    method_number = 0
    def __init__(self, tcParamInstance = None ):
        self.params = None
        if tcParamInstance is None:
            print('Error in ', __name__)
            exit(1)
        self.params = tcParamInstance
        
        self.scriptName = self.params.testCase
        self.script_file = None
        print('Generate script name is : ', self.scriptName)

    def generateCase(self, testCaseName, txPortName, rxPortName, sendIfConfig, receiveIfConfig):
        self.template = string.Template(
            """
import unittest, os, sys, time
                                        
class ${testCaseName}(unittest.TestCase):
    def setUp(self):
        self.sendPort = Port.create("${txPortName}")
        self.receivedPort = Port.create("${rxPortName}")                            
        #self.sendPort.open("${sendIfConfig}")
        #self.receivedPort.open("${receiveIfConfig}")

    def tearDown(self) -> None:
        pass
        #self.sendPort.close()
        #self.receivedPort.close()
    """
    )
        
        self.result = self.template.safe_substitute(testCaseName = testCaseName, txPortName = txPortName, rxPortName = rxPortName, \
                                                    sendIfConfig = sendIfConfig, receiveIfConfig = receiveIfConfig)
        with open(self.scriptName, 'w') as self.script_file:
            self.script_file.write(self.result)



    def appendMethod(self, method_name = 'testMethod', SendValue = '', exceptValue = ''):            
        self.template = string.Template("""
    def ${method_name}(self):
        self.rcvValue = self.sendPort.syncSession("${SendValue}")
        assertIn("${exceptValue}", self.rcvValue)
    """)
        
        self.result = self.template.safe_substitute( method_name = method_name + str(self.method_number),
                                                    SendValue= SendValue, exceptValue =exceptValue )
        with open(self.scriptName, 'a') as self.script_file:
            self.script_file.write(self.result)
        self.method_number = self.method_number + 1

if __name__ == '__main__':  # 未执行的
    # We must create a parameter module
    param = ParamsOneCase()
    dictMethod = {}
    dictMethod['send_interface'] = 'uart'
    dictMethod['send_value'] = 'command string'
    dictMethod['expected_value'] = 'OK'
    dictMethod['receivdd_interface'] = 'can'
    dictMethod['description'] = 'This is a simple description.'
    param.addTestMethod(dictMethod)
    print(param.at(0))

    myTcGenerator = TcGenerator(tcParamInstance=param)
    myTcGenerator.generateCase('testCaseTyp','uart', 'can', 'config for send', 'config for received')
    myTcGenerator.appendMethod(SendValue='cmd', exceptValue = 'OK')

    myTcGenerator.appendMethod('MytestMethod', 'cmd' , 'OK')
    

    
    
    # testGen = TcGenerator()
    # testGen.generateCase('uart', 'can', 'config for send', 'config for received')