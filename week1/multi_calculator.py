import sys
from multiprocessing import Process, Queue

queue1 = Queue()
queue2 = Queue()

def get_userdata(userdatafile):
    with open(userdatafile, 'r') as file:
        for line in file:
            user_list1 = line.strip().split(',')
            queue1.put(user_list)


def calculate(configfile):
    config_dict = {}

    while !queue1.empty():
       user_list2 = queue1.get()
       user_list2[1] = int(user_list2[1])




def dumptofile():
    


if __name__ == '__main__':
    argvs = sys.argv[1:]
    index = argvs.index('-c')
    configfile = argvs[index+1]
    index = argvs.index('-d')
    userdatafile = argvs[index+1]
    index = argvs.index('-o')
    outputfile = argvs[index+1]

    p1 = Process(target=get_userdata, args=(userdatafile,))
    p2 = Process(target=calculate, args=(configfile,))
    p3 = Process(target=dumptofile, args=(,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
	
	


