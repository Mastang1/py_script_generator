import unittest

class Port:

    @staticmethod
    def create(self, port_name = 'uart'):
        if port_name == 'uart':
            pass
        else:
            pass



class TfcTestCase(unittest.TestCase):
    def setUp(self):
        self.sendPort = Port.create(${txPortName})
        self.receivedPort = Port.create(${rxPortName})                            
        #self.sendPort.open(${sendIfConfig})
        #self.receivedPort.open(${receiveIfConfig})

    def tearDown(self) -> None:
        pass
        #self.sendPort.close()
        #self.receivedPort.close()

    def ${method_name}(self):
        self.${receivedValue} = self.sendPort.syncSession(${SendValue})
        assertIn(${exceptValue}, self.${receivedValue})




if __name__ == '__main__':  # 未执行的
    unittest.main()
    

