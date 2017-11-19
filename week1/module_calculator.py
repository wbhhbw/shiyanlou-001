import sys, time, getopt, configparser
from multiprocessing import Process, Queue
from datetime import datetime

def get_userdata(userdatafile):
    with open(userdatafile, 'r') as file:
        for line in file:
            user_list1 = line.strip().split(',')

            queue1.put(user_list1)

def calculate(configfile, city, cp):
    # parser the configfile with configparser
    cp.read(configfile)

    # mark the calculate time
    t = datetime.now()

    #calculate insurance ratio
    ratio = 0
    for k in cp[city]:
        if float(cp[city][k]) < 1:
            ratio += float(cp[city][k])

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
        if salary < float(cp[city]['JiShuL']):
            insur = float(cp[city]['JiShuL']) * ratio
        elif salary > float(cp[city]['JiShuH']):
            insur = float(cp[city]['JiShuH']) * ratio
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
        user_list2.append(datetime.strftime(t, "%Y-%m-%d %H:%M:%S"))

        queue2.put(user_list2)

def dumptofile(outputfile):
    with open(outputfile, 'w') as file:
        if queue2.empty():
            time.sleep(0.2)
        while queue2.empty() == False:
            user_data = queue2.get()
            file.write(str(user_data).strip('[]').replace('\'','')+'\n')

if __name__ == '__main__':
    try:
        queue1 = Queue()
        queue2 = Queue()

        city = None
        configfile = None
        userdatafile = None
        outputfile = None
        cp = configparser.ConfigParser()

        try:
            opts, args = getopt.getopt(sys.argv[1:], 'C:c:d:o:h:', ['help'])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            sys.exit(2)
        for o, a in opts:
            if o == '-C':
                city = a.upper()
            elif o == '-c':
                configfile = a
            elif o == '-d':
                userdatafile = a
            elif o == '-o':
                outputfile = a
            elif o in ('-h', '--help'):
                print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
                sys.exit()

        if city is None:
            city = 'DEFAULT'    

        p1 = Process(target=get_userdata, args=(userdatafile,))
        p2 = Process(target=calculate, args=(configfile, city, cp))
        p3 = Process(target=dumptofile, args=(outputfile,))

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()
    except ValueError as e:
        print("except:", e)
    except FileNotFoundError as e:
        print("except:", e)