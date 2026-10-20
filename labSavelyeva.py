
import re
import math

expr = input("Выражение: ").replace(' ', '')
elements = re.findall(r'\d+\.\d+|\d+|sin|<=|[-+*/()]', expr)
nums = []
ops = []

pos = 0
while pos < len(elements):
    el = elements[pos]
    if el[0].isdigit():
        nums.append(float(el))
    elif el == '(':
        ops.append(el)
    elif el == 'sin':
        pos += 1
        nums.append(math.sin(float(elements[pos])))
    elif el in '+-*/<=':
        if el == '-' and (pos == 0 or elements[pos-1] in '+-*/('):
            nums.append(0)
            
        while ops and ops[-1] in '+-*/<=' and (ops[-1] in '*/' or (ops[-1] in '+-' and el in '+-<=') or (ops[-1] == '<=')):
            op = ops.pop()
            if op == 'sin':
                nums.append(math.sin(nums.pop()))
                continue
                
            b = nums.pop()
            a = nums.pop()
            if op == '+': nums.append(a + b)
            elif op == '-': nums.append(a - b)
            elif op == '*': nums.append(a * b)
            elif op == '/': nums.append(a / b)
            elif op == '<=': nums.append(1 if a <= b else 0)
        ops.append(el)
        
    elif el == ')':
        print(ops)
        while ops[-1] != '(':
            op = ops.pop()
            print(op)
            b = nums.pop()
            a = nums.pop()
            if op == '+': nums.append(a + b)
            elif op == '-': nums.append(a - b)
            elif op == '*': nums.append(a * b)
            elif op == '/': nums.append(a / b)
            elif op == '<=': nums.append(1 if a <= b else 0)
        ops.pop()
        if ops and ops[-1] == 'sin':
            ops.pop()
            nums.append(math.sin(nums.pop()))
        
    pos += 1


while ops:
    op = ops.pop()
    if op == 'sin':
        nums.append(math.sin(nums.pop()))
        continue
    b = nums.pop()
    a = nums.pop()
    if op == '+': nums.append(a + b)
    elif op == '-': nums.append(a - b)
    elif op == '*': nums.append(a * b)
    elif op == '/': nums.append(a / b)
    elif op == '<=': nums.append(1 if a <= b else 0)

res = nums[0]
print(int(res) if res.is_integer() else res)