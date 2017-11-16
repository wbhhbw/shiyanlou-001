#!/usr/bin/env python3

import sys

#Define a function to calculate the insurance
def calc_insurance(salary):
    return salary*(0.08+0.02+0.005+0.06)

#Define a function to calculates the tax
def calc_tax(salary):
    pay = salary - calc_insurance(salary) - 3500
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
    return tax

#获取工资数额
try:
    argvs = sys.argv[1:]
    for arg in argvs:
        items = arg.split(':')
        work_id = int(items[0])
        salary = int(items[1])
        #计算个税
        money = salary - calc_tax(salary) - calc_insurance(salary)
        print("%d:%.2f " % (work_id, money))
    
except ValueError:
    print("Parameter Error")

