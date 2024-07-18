import unittest



class testCaseTyp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(" ================== test begin ===================")
        
    @classmethod
    def tearDownClass(cls):
        print(" ================== test end ===================")

    def setUp(self) -> None:
        print(' ----------setup')
        foo = getattr(self, self._testMethodName, None)
        if foo:
            print('Return is :', foo(getParam = True) )
            # Then, do something , and excute some process
        
    def tearDown(self) -> None:
        print('teardown')
    



    def testMethod0(self, getParam = False):
        if getParam is True:
            print(" called by setUp(0)")
            return 0
        else:

            print('This is a test method0.')
            self.assertEqual(1, 1)

    def testMethod1(self, getParam = False):
        if getParam is True:
            print(" called by setUp(1)")
            pravitedParam = 1111
            return pravitedParam
        else:

            print('This is a test method1.')
            self.assertEqual(1, 1)

    def testMethod2(self, getParam = False):
        if getParam is True:
            print(" called by setUp(2)")
            return 2
        else:
            print('This is a test method2.')
            self.assertEqual(1, 1)



def addTestCastM1():
    # 实例化
    suite = unittest.TestSuite()
    # 调用添加方法
    # 写法一: suite.addTest(类名(“方法名”)) 注意:方法名称使用双引号
    # suite.addTest(Test01("test_add"))
    # suite.addTest(unittest.makeSuite(testCaseTyp))
    # suite.addTest(testCaseTyp("testMethod0"))
    suite.addTest(testCaseTyp("testMethod0"))
    suite.addTest(testCaseTyp("testMethod1"))
    suite.addTest(testCaseTyp("testMethod2"))



    # suite.addTest(unittest.makeSuite(test_case2.Test02))
    # 法二:suite.addTest(unittest.makeSuite(类名)) 添加指定类中所有已test开头的方法
    # suite.addTest(unittest.makeSuite(test_case1.Test01))
    unittest.TextTestRunner().run(suite)



if __name__ == '__main__':
    
    dictTest = {}
    dictTest['first'] = 'nice'
    dictTest['second'] = 'day'

    strTest = str(dictTest)
    print(strTest, type(strTest))
    print(dictTest, type(dictTest))


