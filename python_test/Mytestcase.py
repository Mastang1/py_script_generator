
import unittest, os, sys, time

class testCaseTyp(unittest.TestCase):
    '''
    This is a class, create ...
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
        
        self.txPort = DevFactory.createDevIf(methodParam['txIfName'])
        self.rxPort = DevFactory.createDevIf(methodParam['rxIfName'])   
        
        # Open by default                         
        # self.txPort.open()
        # self.rxPort.open()

    def tearDown(self) -> None:
        self.txPort.close()
        self.rxPort.close()
    