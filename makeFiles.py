import time
import random
import os
import glob
import shutil


def changeBase(num, base=36):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = ""
    total = num
    i = 0
    while total != 0:
        d = int((num / base**i) % base)
        total -= d * base**i
        out = digits[d] + out
        i += 1
    return out

def formatStr(s, num):
    return ("0" * (num - len(s))) + s


def createName(num):
    return formatStr( changeBase(num) , 4)


def nameToNum(name):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = 0
    for i in range(len(name)):
        num += digits.find(name[i*-1 - 1]) * (len(digits)**i)
    return num

def inv(num):
    return 127 - num 

def zeros(name, folder="D:\\Reserved Space", size=1024**3):
    n = createName(name)
    f = open(os.path.join(folder,n+".res"),"wb+")
    f.write( bytearray(size) )
    f.close()

def ones(name, folder="D:\\Reserved Space", size=1024**3):
    n = createName(name)
    f = open(os.path.join(folder,n+".res"),"wb+")
    f.write( bytearray(b'\xff') * size )
    f.close()

def random(name, folder="D:\\Reserved Space", size=1024**3):
    n = createName(name)
    f = open(os.path.join(folder,n+".res"),"wb+")
    f.write( os.urandom(size) )
    f.close()

def complimentLast(name, folder="D:\\Reserved Space"):
    fNot = open(os.path.join(folder,createName(name)+".res"), 'wb')
    with open(os.path.join(folder,createName(name - 1)+".res"), 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            fNot.write(bytes([inv(ord(byte))]))
    fNot.close()

def fullFile(name, folder, size=1024**3):
    if not os.path.exists("data/algorithm.dat"):
        zeros(name,folder,size)
        ones(name,folder,size)
        random(name,folder,size)
        zeros(name,folder,size)
        random(name,folder,size)
    else:
        funcDict = dict()
        funcDict["0"] = zeros
        funcDict["1"] = ones
        funcDict["r"] = random
        f = open("data/algorithm.dat")
        algo = f.read()
        f.close()
        for c in algo:
            if c in funcDict.keys():
                funcDict[c](name,folder,size)





def copyLast(name, folder="D:\\Reserved Space"):
    shutil.copy(os.path.join(folder,createName(name - 1)+".res"), os.path.join(folder,createName(name)+".res"))
