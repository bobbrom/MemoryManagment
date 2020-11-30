from flask import Flask, render_template, request, jsonify, render_template
import psutil
import glob
import os
import sys
import makeFiles
import time
import threading
import math


def getReserved():
    folder = open("mainFolder.dat").read()
    files = []
    for f in os.walk(folder):
        files += [os.path.join(f[0], a) for a in f[-1]]

    return sum([os.path.getsize(a) for a in files])


os.chdir(os.path.dirname(os.path.abspath(__file__)))
hdd = psutil.disk_usage("D:\\")

folder = open("data/mainFolder.dat").read()


#os.chdir(folder)

reserved = getReserved()

print(reserved)

total = hdd.total
used  = hdd.used
free  = hdd.free - reserved



reservedPerc = round((100/total)*getReserved(),2)
usedPerc     = round((100/total)*used,2)
freePerc     = round((100/total)*free,2)
available    = round((reserved+free)/1024**3)





app = Flask(__name__)
@app.route("/")
def index():
    folder = open("data/mainFolder.dat").read()
    hdd = psutil.disk_usage("D:\\")

    reserved = getReserved()

    total = hdd.total
    used  = hdd.used - reserved
    free  = hdd.free

    selected = ""
    if (os.path.exists(os.path.join(os.getenv('ProgramData'), "Microsoft\\Windows\\Start Menu\\Programs\\StartUp",
                                    "MemoryManagment.bat"))):
        selected = "checked"

    reservedPerc = round((100/total)*reserved,2)
    usedPerc     = round((100/total)*used,2)
    freePerc     = round((100/total)*free,2)
    available    = round((reserved+free)/1024**3)
    return render_template("index.html",
                           usedPerc=usedPerc,
                           reservedPerc=40,
                           freePerc=freePerc,
                           total   =round(total/1024**3),
                           used    =round(used/1024**3),
                           free    =round(free/1024**3),
                           reserved=round(reserved/1024**3),
                           selected=selected,
                           available=round((reserved+free)/1024**3)
                           )

@app.route('/refresh', methods=['POST'])
def refresh():
    print("AAAA")


ticks = 1
times = [0] * 5

done = 0

# def writeFolder(name, folder, size):
#     global ticks
#     global times
#     global done
#
#     r = glob.glob("D:\\Reserved Space\\*.res")
#     r = [a.split("\\")[-1].split(".")[0] for a in r]
#
#     last = r[-1]
#     last = makeFiles.nameToNum(last)
#     for i in range(round(size)):
#         j = last + i + 1
#
#         start = time.time_ns()
#         makeFiles.zeros(name)
#         ticks += 1
#         stop = time.time_ns()
#
#         times[0] = stop - start
#
#         start = time.time_ns()
#         makeFiles.ones(name)
#         ticks += 1
#         stop = time.time_ns()
#
#         times[1] = stop - start
#
#         start = time.time_ns()
#         makeFiles.random(name)
#         ticks += 1
#         stop = time.time_ns()
#
#         times[2] = stop - start
#
#         start = time.time_ns()
#         makeFiles.zeros(name)
#         ticks += 1
#         stop = time.time_ns()
#
#         times[3] = stop - start
#
#         start = time.time_ns()
#         makeFiles.random(name)
#         ticks += 1
#         stop = time.time_ns()
#
#         times[4] = stop - start
#
#         done += 1

def write(size, folder="D:\\Reserved Space", file_size=1024**3):
    p = ["b","kb","mb","gb"]
    amounts = []
    free = hdd.free
    for i in range(4):
        bytesFree = free % 1024**(i+1)
        amount = bytesFree / 1024**(i)
        free -= bytesFree

        writeFolder(folder, size)

        print(p[i],free)
        amounts.append(amount)


# def write(size, folder="D:\\Reserved Space", file_size=1024**3):
#     global ticks
#     global times
#     global done
#     r = glob.glob("D:\\Reserved Space\\*.res")
#     r = [a.split("\\")[-1].split(".")[0] for a in r]
#
#     last = r[-1]
#     last = makeFiles.nameToNum(last)
#
#     for i in range(round(size)):
#         j = last + i + 1
#         writeFile(j, folder, file_size)



#reserveFreeSpace
amountToReserve = 1
@app.route('/reserveFreeSpace', methods=['POST'])
def reserveFreeSpace():
    global amountToReserve
    reserved = getReserved()
    global available

    available    = round((reserved+free)/1024**3)
    amountToKeepFree = float(request.form['amountToReserve'])
    print(amountToReserve)
    option = request.form['type']
    print(option)
    
    if option == "percent_free":
        amountToKeepFree = available * (amountToReserve/100)
    if option == "Gb_keep":
        amountToKeepFree = available - amountToKeepFree

    f = open(os.path.join(folder, "keepFree.dat"), "w")
    f.write(str(amountToKeepFree))



    return render_template("reserveFreeSpace.html",amountToReserve=amountToReserve)


    
@app.route('/_add_numbers')
def add_numbers():
    perc = (100 / (amountToReserve*5))*ticks

    amountToDo = amountToReserve - done
    
    if(done < 1):
        div = len([i for i in times if i != 0])*sum(times)
        if(div != 0):
            eta = (float(len(times))/float(div))*amountToDo
        else:
            eta = 0
    else:
        eta = amountToDo * sum(times)
    eta = round((eta / 10**9)/60, 2)
    perc = round(perc, 2)
    return jsonify(result=perc,eta=eta,done=done)


if __name__ == "__main__":
    app.run()
