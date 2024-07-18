import os, sys, time

def sub(arg = 'hello'):
    print(arg)

def testArg(*args, **kwargs):
    sub(*args, **kwargs)

def testList():
    try:
        a = input("输入一个数：")
        #判断用户输入的是否为数字
        if(not a.isdigit()):
            raise ValueError("a 必须是数字")
    except ValueError as e:
        print("引发异常：",repr(e))

    print("Next ...")

if __name__ == '__main__':
    testList()
    