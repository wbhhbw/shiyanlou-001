import sys, time
from multiprocessing import Process, Queue


def get_userdata(userdatafile):
    with open(userdatafile, 'r') as file:
        for line in file:
            user_list1 = line.strip().split(',')

            queue1.put(user_list1)


def calculate(configfile):
    config_dict = {}
    with open(configfile, 'r') as file:
        for line in file:
            conf_list =  line.strip().split('=')
            config_dict[conf_list[0].strip()] = float(conf_list[1])


    #calculate insurance ratio
    ratio = 0
    for x in config_dict.values():
        if x < 1:
            ratio += x


    #calculate insur and tax then construct a new list
    if queue1.empty():
        time.sleep(0.1)
    while queue1.empty() == False:
        user_list2 = queue1.get()
        salary = int(user_list2[1])

        insur = 0
        pay = 0 
        tax = 0

        #calculate insurance
        if salary < config_dict['JiShuL']:
            insur = config_dict['JiShuL'] * ratio
        elif salary > config_dict['JiShuH']:
            insur = config_dict['JiShuH'] * ratio
        else:
            insur = salary * ratio

        #calculate tax
        pay = salary - insur - 3500
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
        
        user_list2.append('{:.2f}'.format(insur))
        user_list2.append('{:.2f}'.format(tax))
        user_list2.append('{:.2f}'.format(salary - tax- insur))

        queue2.put(user_list2)





def dumptofile(outputfile):
    with open(outputfile, 'w') as file:
        if queue2.empty():
            time.sleep(0.2)
        while queue2.empty() == False:
            user_data = queue2.get()
            file.write(str(user_data).strip('[]').replace(' ','').replace('\'','')+'\n')

    


if __name__ == '__main__':
    queue1 = Queue()
    queue2 = Queue()

    argvs = sys.argv[1:]
    index = argvs.index('-c')
    configfile = argvs[index+1]
    index = argvs.index('-d')
    userdatafile = argvs[index+1]
    index = argvs.index('-o')
    outputfile = argvs[index+1]

    p1 = Process(target=get_userdata, args=(userdatafile,))
    p2 = Process(target=calculate, args=(configfile,))
    p3 = Process(target=dumptofile, args=(outputfile,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

