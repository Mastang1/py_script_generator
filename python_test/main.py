import unittest
from . import test_case1


def addTestCastM1():
    # 实例化
    suite = unittest.TestSuite()
    # 调用添加方法
    # 写法一: suite.addTest(类名(“方法名”)) 注意:方法名称使用双引号
    # suite.addTest(Test01("test_add"))
    suite.addTest(test_case1.Test01("test_add2"))
    # suite.addTest(unittest.makeSuite(test_case2.Test02))
    # 法二:suite.addTest(unittest.makeSuite(类名)) 添加指定类中所有已test开头的方法
    # suite.addTest(unittest.makeSuite(test_case1.Test01))
    unittest.TextTestRunner().run(suite)

def discoveryTestCase():
    combinSuite = unittest.TestLoader().discover("./Tcs", "test_case*.py")
    # combinSuite = combinSuite + unittest.TestLoader().discover("./test_cases", "test_case2*.py")
    # combinSuite = combinSuite + unittest.TestLoader().discover("./test_cases", "test_case3*.py")

    # 推荐使用
    # suite = unittest.defaultTestLoader.discover("../cases")

    unittest.TextTestRunner().run(combinSuite)


if __name__ == '__main__':
    # addTestCastM1()
    discoveryTestCase()

