#!/usr/bin/env python3

import sys

#Config class, used to get and store the information in the configfile
class Config(object):
    def __init__(self, configfile):
        self._config = {}
        with open(configfile, 'r') as file:
            for line in file:
                conf_list =  line.strip().split('=')
                self._config[conf_list[0].strip()] = int(conf_list[1])

    # get config data
    def get_config(self, para):
        return self._config[para]

    def get_configs(self):
        return self._config

#UserData class, used to get and store employee data
class UserData(object):
    def __init__(self, userdatafile):
        self._userdata = {}
        with open(userdatafile, 'r') as file:
            for line in file:
                user_list = line.strp().split(',')
                self._userdata[int(user_list[0])] = int(user_list[1]) 

    def get_userdata(self, para):
        return self._userdata[para]

    def get_userdatas(self):
        return self._userdata

#calculator class, used to calculate social insurance and taxes
class calculator(object):
    def __init__(self):
        self.insr_dict = {}
        self.tax_dict = {}

    #Define a function to calculate the insurance then stroe in insr_dict{}
    def calc_insurance(self, user, conf):
        for k,v in user.get_userdatas().items():
            if v < conf.get_config('JishuL')




    #Define a function to calculates the tax
    def calc_tax(self, salary):
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

