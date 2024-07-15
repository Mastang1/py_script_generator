
class ParamsOneCase:
    '''
    The class includes all parameters of a sheet.
    '''
    def __init__(self, testcaseName = "Mytestcase.py"):
        self.testCase = testcaseName
        self.testMethodNum = 0
        self.methodGrp = []

    def addTestMethod(self, dictMethod = {}):
        self.methodGrp.append(dictMethod)
        self.testMethodNum = self.testMethodNum + 1


    def at(self, index):
        if index > self.testMethodNum - 1:
            return None
        return self.methodGrp[index]

if __name__ == '__main__':
    ParamsOneCase()


