import glob

import psutil
import os
from python import makeFiles
import time
import sys





def toGB(size):
    return round(size / 1024 ** 3)

def toBytes(size):
    return size * 1024 ** 3

locked = True

while(locked):
    try:
        hdd = psutil.disk_usage("D:\\")
        locked = False
    except:
        print("Nope")
        locked = True
        time.sleep(1)

os.chdir(os.path.dirname(os.path.abspath(__file__)))



def writePID():
    pid = os.getpid()
    pid_file = "../data/pid_background.dat"
    f = open(pid_file,"w+")
    f.write(str(pid))
    f.close()






folder = open("../data/mainFolder.dat").read()

# print("----->",folder)
reserved = sum([os.path.getsize(a) for a in glob.glob(os.path.join(folder,"*"))])


amountToBeFree = float(open("../data/keepFree.dat").read())


total    = hdd.total
used     = hdd.used
avalible = hdd.used - reserved

toDo = hdd.free - toBytes(amountToBeFree)


def getAmounts(bytesToDo):
    amountsMade = []
    for i in range(4):
        bytesFree = bytesToDo % 1024**(i+1)
        amount = bytesFree // 1024**(i)
        bytesToDo -= bytesFree
        amountsMade.append(int(amount))
    return amountsMade




units = ["B", "KB", "MB", "GB"]
amountsMade = []
bytesToDo = hdd.free - toBytes(amountToBeFree)
def run(forever):
    writePID()
    while(True):
        hdd = psutil.disk_usage("D:\\")
        amountToBeFree = float(open("../data/keepFree.dat").read())

        f = open("../data/wasFree.dat", "w+")
        f.write(str(hdd.free))
        f.close()


        bytesToDo = hdd.free - toBytes(amountToBeFree)

        if(bytesToDo > 2*1024**2):
            print("Making:",bytesToDo)
            # amountsMade = getAmounts(bytesToDo)
            # print(amountsMade)
            i = 0
            first = True
            test = 0
            # print("--", len(units))
            for i in range(len(units)):
                # print("------------->",i)
                i = len(units) - i -1


                this_folder = os.path.join(folder, units[i])
                if not os.path.exists(this_folder):
                    os.mkdir(this_folder)

                r = glob.glob(os.path.join(this_folder,"*.res"))

                r = [a.split("\\")[-1].split(".")[0] for a in r]


                if(len(r) != 0):
                    last = r[-1]
                    last = makeFiles.nameToNum(last)
                else:
                    last = 0

                z = 0
                amount = 100

                hdd = psutil.disk_usage("D:\\")
                bytesToDo = hdd.free - toBytes(amountToBeFree)
                bytesFree = bytesToDo % 1024**(i+1)
                amount = int(bytesFree // 1024**(i))
                for j in range(amount):
                    print((j + 1),"/", amount,"--", os.path.join(folder, units[i]), "--", "1024**" + str(i))
                    makeFiles.fullFile(last + j + 1, os.path.join(folder, units[i]), 1024 ** i)

                    test += (1024**(i))
                    z+= 1
                # print("---->>>>>", units[i], z, amount, i)

                i += 1
            hdd = psutil.disk_usage("D:\\")
            bytesToDo = hdd.free - toBytes(amountToBeFree)
        elif(bytesToDo < 0):
            bytesToDo *= -1
            print("Deleteing:", bytesToDo)
            amountsMade = getAmounts(bytesToDo)
            for i in range(len(units)):
                # print("i:",i)
                r = glob.glob(os.path.join(os.path.join(folder, units[i]), "*.res"))
                r = [a.split("\\")[-1] for a in r]
                print(units[i])
                print(amountsMade[i])
                z = 0
                if(len(r) < amountsMade[i]):
                    print(len(r), "<", amountsMade[i])
                    r = glob.glob(os.path.join(os.path.join(folder, units[i+1]), "*.res"))
                    os.remove(r[-1])
                    amount = 1024 - amountsMade[i]
                    for j in range(amount):
                        print((j + 1), "/", amount, "--", os.path.join(folder, units[i]), "--", "1024**" + str(i))
                        makeFiles.fullFile(j, os.path.join(folder, units[i]), 1024 ** i)
                    continue


                for j in range(amountsMade[i]):
                    try:
                        file = os.path.join(folder, units[i], r[(j * -1 - 1)])
                        print("Deleting:",file)
                        os.remove(file)
                        z += 1
                    except:
                        a = 1
            hdd = psutil.disk_usage("D:\\")
            bytesToDo = hdd.free - toBytes(amountToBeFree)
        else:
            print("No more to do")
            if not forever:
                break
        time.sleep(10)


if __name__ == "__main__":
    if(len(sys.argv) == 0 or sys.argv[0] == "true"):
        run(True)
    else:
        run(False)
