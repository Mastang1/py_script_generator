import string
 
# 定义函数来生成Python脚本
def generate_python_script(function_name, code_lines):
    template = string.Template("""
def ${function_name}():
    ${code_block}
 
# Called the function
${function_name}()
""")
    
    code_block = '\n    '.join(code_lines)
    result = template.safe_substitute(function_name=function_name, code_block=code_block)
    return result
 
# 使用函数生成脚本
code_lines = ["print('Hello, World!')", "x = 10", "y = 20", "print(x + y)" ]
script = generate_python_script('my_function', code_lines)
 
# 打印生成的脚本
print(script)
 
# 将脚本保存到文件
with open('generated_script.py', 'w') as file:
    file.write(script)

'''
def my_function():
    print('Hello, World!')
    x = 10
    y = 20
    print(x + y)
 
# 调用函数
my_function()

'''