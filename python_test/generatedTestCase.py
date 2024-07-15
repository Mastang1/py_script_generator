
import unittest, os, sys, time
                                        
class testCaseTyp(unittest.TestCase):
    def setUp(self):
        self.sendPort = Port.create("uart")
        self.receivedPort = Port.create("can")                            
        #self.sendPort.open("config for send")
        #self.receivedPort.open("config for received")

    def tearDown(self) -> None:
        pass
        #self.sendPort.close()
        #self.receivedPort.close()
    
    def testMethod0(self):
        self.rcvValue = self.sendPort.syncSession("cmd")
        assertIn("OK", self.rcvValue)
    
    def MytestMethod1(self):
        self.rcvValue = self.sendPort.syncSession("cmd")
        assertIn("OK", self.rcvValue)
    