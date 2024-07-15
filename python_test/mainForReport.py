import unittest
from tool_report import HTMLTestRunner
 
# 定义一些测试用例
class TestCaseSheet1(unittest.TestCase):
    def test_one(self):
        self.assertEqual(1, 1)  
    
    def test_two(self):
        self.assertEqual(2, 2)
        
class TestCaseSheet2(unittest.TestCase):
    def test_one(self):
        self.assertEqual(1, 1)
    
    def test_two(self):
        self.assertEqual(2, 2)

# 收集测试用例
def suite():
    # test_suite = unittest.TestSuite()
    test_suite = unittest.TestLoader().discover("./Tcs", "test_case*.py")
    test_suite.addTest(TestCaseSheet1('test_one'))
    test_suite.addTest(TestCaseSheet2('test_two'))
    return test_suite
 
# 运行测试并生成报告
with open('TestReport.html', 'wb') as f:
    runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Test Report', description='Description of this test.')
    runner.run(suite())

