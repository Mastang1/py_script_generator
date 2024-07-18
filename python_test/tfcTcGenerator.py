import string, os, sys
from tfcParamMang import ParamsOneCase


class TcGenerator:
    __templateCase = """
import unittest, os, sys, time

class ${testCaseName}(unittest.TestCase):
    '''
    ${classDescription}
    '''
    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Step1, get parameter from current method
        curMethod = getattr(self, self._testMethodName, None)
        if curMethod:
            methodParam = curMethod(getParam = True)
        
        self.txIf = DevFactory.createDevIf(methodParam['txIfName'])
        self.rxIf = DevFactory.createDevIf(methodParam['rxIfName'])   

        # Open by default                         
        # self.txIf.open()
        # self.rxIf.open()

    def tearDown(self) -> None:
        self.txIf.close()
        self.rxIf.close()
    """

    __templateMethod  = """
    def ${methodName}(self, getParam = False):
        '''
        ${methodDescription}
        '''
        methodParam = ${methodParam}
        if getParam is True:
            return methodParam
        else:
            self.rcvValue = self.sendPort.syncSession(methodParam['txValue'])
            assertIn("${exceptValue}", self.rcvValue)
        
    """
    method_number = 0

    def __init__(self, tcParamInstance = None, scriptFileName = None ):
        self.params = None
        if tcParamInstance is None:
            print('Error in ', __name__)
            exit(1)
        self.params = tcParamInstance
        
        self.scriptName = scriptFileName
        self.scriptFile = None
        print('Generate script name is : ', self.scriptName)

    def generateCase(self, testCaseName, classDescription):
        self.template = string.Template(self.__templateCase)
        self.result = self.template.safe_substitute(testCaseName = testCaseName, classDescription = classDescription)
        with open(self.scriptName, 'w') as self.scriptFile:
            self.scriptFile.write(self.result)

    def appendMethod(self, methodParam = None):            
        self.template = string.Template(self.__templateMethod)
        
        self.result = self.template.safe_substitute( methodName = methodParam['methodName'] + str(self.method_number), 
                methodDescription = methodParam['methodDescription'], methodParam = str(methodParam), exceptValue = methodParam['expectedValue'] )
        with open(self.scriptName, 'a') as self.scriptFile:
            self.scriptFile.write(self.result)
        self.method_number = self.method_number + 1

if __name__ == '__main__':  # 未执行的
    # We must create a parameter module
    param = ParamsOneCase(testcaseName= 'testCaseCan2Can')

    for i in range(10):
        dictMethod = {}
        dictMethod['methodName'] = 'testMethod'
        dictMethod['txIfName'] = 'uart'
        dictMethod['txIfConfig'] = 'config tx interface'
        dictMethod['txValue'] = 'command string'
        dictMethod['expectedValue'] = 'OK'
        dictMethod['rxIfName'] = 'can'
        dictMethod['rxIfConfig'] = 'config tx interface'
        dictMethod['methodDescription'] = 'This is a simple description:' + str(i)
        param.addTestMethod(dictMethod)
        print('Test parameter:',param(i)['methodDescription'])

    myTcGenerator = TcGenerator(tcParamInstance=param, scriptFileName="fight.py")
    myTcGenerator.generateCase(param.testCaseName,'This is a class, create ...')

    for j in range(10):
        myTcGenerator.appendMethod(param(j))
        print(param(j)['methodDescription'])
