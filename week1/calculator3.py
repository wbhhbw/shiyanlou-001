#!/usr/bin/env python3

import sys

#Config class, used to get and store the information in the configfile
class Config(object):
    def __init__(self, configfile):
        self._config = {}
        with open(configfile, 'r') as file:
            for line in file:
                conf_list =  line.strip().split('=')
                self._config[conf_list[0].strip()] = float(conf_list[1])

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
                user_list = line.strip().split(',')
                self._userdata[user_list[0].strip()] = int(user_list[1]) 

    def get_userdata(self, para):
        return self._userdata[para]

    def get_userdatas(self):
        return self._userdata

#calculator class, used to calculate social insurance and taxes
class Calculator(object):
    def __init__(self):
        self._insur_dict = {}
        self._tax_dict = {}       

    #Define a function to calculate the insurance and tax then stroe in insur_dict{} and tax_dict{}
    def calculate(self, user, conf):
        ratio = 0
        for x in conf.get_configs().values():
            if x < 1:
                ratio += x

        insur = 0
        pay = 0 
        tax = 0            
        for k,v in user.get_userdatas().items():            
            if v < conf.get_config('JishuL'):
                insur = conf.get_config('JishuL') * ratio
            elif v > conf.get_config('JishuH'):
                insur = conf.get_config('JishuH') * ratio
            else:
                insur = v * ratio

            pay = v - insur - 3500
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
            self._insur_dict[k] = insur
            self._tax_dict[k] = tax

    def get_insur_dict(self):
        return self._insur_dict

    def get_insur_dict_data(self, para):
        return self._insur_dict[para]

    def get_tax_dict(self):
        return self._tax_dict

    def get_tax_dict_data(self, para):
        return self._tax_dict[para]

#Define an output class
class Outputor(object):
    def __init__(self, outputfile):
        self._outputfile = outputfile

    def dumptofile(self, user, calc):
        with open(self._outputfile, 'w') as file:
            for num in user.get_userdatas().keys():
                file.write(str(num)+','+str(user.get_userdata(num))+','\
                    +'{:.2f}'.format(calc.get_insur_dict_data(num))+','\
                    +'{:.2f}'.format(calc.get_tax_dict_data(num))+','\
                    +'{:.2f}'.format(user.get_userdata(num)-calc.get_insur_dict_data(num)-calc.get_tax_dict_data(num))+'\n')
    
    

try:
    argvs = sys.argv[1:]
    index = argvs.index('-c')
    configfile = argvs[index+1]
    index = argvs.index('-d')
    userdatafile = argvs[index+1]
    index = argvs.index('-o')
    outputfile = argvs[index+1]
    config = Config(configfile)
    userdata = UserData(userdatafile)
    calculator = Calculator()
    output = Outputor(outputfile)
    calculator.calculate(userdata, config)
    output.dumptofile(userdata, calculator)
    
except ValueError:
    print("Parameter Error")
except FileNotFoundError:
    print("FileNotFound Error") 

