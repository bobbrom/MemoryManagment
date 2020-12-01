import time
import struct

f = open("D:\\Reserved Space\\00KG.res","rb")
##print(f.read()[0:20])


##start = time.time()
##f1 = open("D:\\test.res","wb")
##with open("D:\\Reserved Space\\00KG.res", 'rb') as infile, open("D:\\test.res", 'wb') as of:
##    while True:
##        d = infile.read(4)
##        if not d:
##            break
##        le = struct.unpack('<I', d)
##        be = struct.pack('>I', *le)
##        of.write(be)
##stop = time.time()
##
##print(stop - start)
##
f1 = open("D:\\test.res","rb")
##
a = bin(int.from_bytes(f.read()[0:10], byteorder="big"))
b = bin(int.from_bytes(f1.read()[0:10], byteorder="big"))

print(a)
print(b)

