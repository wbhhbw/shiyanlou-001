#!/usr/bin/env python3

import sys

#获取工资数额
temp  = sys.argv[1]

#参数校验
try:
    salary = int(temp)
    #计算个税
    pay = salary - 0 - 3500
    if pay <= 0:
        tax = 0
    elif pay > 0 and pay <= 1500:
        tax = pay * 0.03 - 0
    elif pay > 1500 and pay <= 4500:
        tax = pay * 0.1 - 105
    elif pay >4500 and pay <= 9000:
        tax = pay * 0.2 - 55
    elif pay > 9000 and pay <= 35000:
        tax = pay * 0.25 - 1005
    elif pay > 35000 and pay <= 55000:
        tax = pay * 0.3 - 2755
    elif pay > 55000 and pay <= 80000:
        tax = pay * 0.35 - 5505
    else:
        tax  = pay * 0.45 - 13505

    #输出
    print("%.2f" % tax)
except ValueError:
    print("Parameter Error")

