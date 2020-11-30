import psutil
# import glob
# import os
# import sys
# import makeFiles
# import time
# import threading
import os


#2298
#
# import psutil
#
#
# f = open("data/pid_background.dat")
pid = 16964
# f.close()
running = False
for p in psutil.process_iter(attrs=["pid"]):
    if p.pid == pid:
        print(p)
#
print(running)



# if( os.path.exists(os.path.join(os.getenv('ProgramData'),"Microsoft\\Windows\\Start Menu\\Programs\\StartUp","MemoryManagment.bat")) ):
#     selected = "selected"
from shutil import copyfile

# os.chdir(os.path.dirname(os.path.abspath(__file__)))
#
# dst = os.path.join(os.getenv('ProgramData'),"Microsoft\\Windows\\Start Menu\\Programs\\StartUp","MemoryManagment.bat")
# copyfile("MemoryManagment.bat", dst)


# file_folder = __file__.split("/")
# file_folder.pop()
# file_folder = os.sep.join(file_folder)
#
# bat_file = os.path.join(file_folder,"MemoryManagment.bat")
# if not os.path.exists(bat_file):
#     cmd = os.path.join(file_folder,"venv","Scripts","pythonw.exe")
#     background_file = os.path.join(file_folder,"background.py")
#     f = open(bat_file,"w+")
#     f.write(cmd+" "+background_file)
#     f.close()


# os.system("echo aaaa")

# print(os.getenv('ProgramData'))
#
# f = glob.glob()
# print(f)

#
# selected = ""
# if( os.path.exists(os.path.join(os.getenv('ProgramData'),"Microsoft\\Windows\\Start Menu\\Programs\\StartUp","MemoryManagment.bat")) ):
#     selected = "selected"


# folder = "D:\\Reserved Space"
#
# mb_folder = os.path.join(folder,"mb")
#
# if not os.path.exists( mb_folder ):
#     os.mkdir(mb_folder)
#
#
#

# locked = True
# while(locked):
#     try:
#         hdd = psutil.disk_usage("D:\\")
#         locked = False
#     except:
#         print("Nope")
#         locked = True
#         time.sleep(1)
#
# print(hdd)
# def getReserved():
#     folder = open("mainFolder.dat").read()
#     files = []
#     for f in os.walk(folder):
#         files += [os.path.join(f[0],a) for a in f[-1]]
#
#     return sum([os.path.getsize(a) for a in files])


# a = makeFiles.nameToNum("01RU")
#
#
# start = time.time_ns()
# makeFiles.copyLast(2299)
# stop = time.time_ns()
# print((stop - start)/10**9)
#
#
# start = time.time_ns()
# makeFiles.complimentLast(2299)
# stop = time.time_ns()
# print((stop - start)/10**9)


##def binS(num):
##    out = ""
##    while len(out) < 7:
##        out = str(num & 1) + out
##        num = num >> 1        
##    return out
##
##
##def inv(num):
##    return 127 - num 
##
##
##
##
##out = ""
##
##folder = "D:\\Reserved Space"
##
##fNot = open(os.path.join(folder,createName(name)+".res"), 'wb')
##with open(os.path.join(folder,createName(name - 1)+".res"), 'rb') as f:
##    while True:
##        byte = f.read(1)
##        if not byte:
##            break
##        fNot.write(bytes([inv(ord(byte))]))
##fNot.close()
##
##print(out)
##print()
##out2 = ""
##
##with open("D:\\Reserved Space\\test2.txt", 'rb') as f:
##    while True:
##        byte = f.read(1)
##        if not byte:
##            break
##        out2 += binS(ord(byte)) + " "
##print(out2)
##                   
##
##
