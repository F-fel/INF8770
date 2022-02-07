"""
This is the driver for our project
"""
from time import process_time
from generator import Generator
from RLE import RLE
from LZ77 import LZ77
import csv
import os
import random
MIN_SIZE = 1024
MAX_SIZE = 5120
DATA_DIR = "DATA"
LZ_DIR = "LZ77"
RLE_DIR = "RLE"
sampleFactory = Generator(255)
stats = {}
# compressors
compressorRLE = RLE()
compressorLZ  = LZ77()
def make_clean():
    # delete all files in the utput directories
    for filename in os.listdir(LZ_DIR):
        os.remove(LZ_DIR+'/'+filename)
    for filename in os.listdir(RLE_DIR):
        os.remove(RLE_DIR+'/'+filename)
def generateRandomSamples(nSamples):
    # generate samples with random text and size between MIN_SIZE and MAX_SIZE bytes
    for x in range(nSamples):
        length = random.randint(MIN_SIZE,MAX_SIZE)
        txt = sampleFactory.generate(length)
        file = open(DATA_DIR + "/sample"+str(x), "w")
        file.write(txt)
        file.close()
def generateSimpleSamples():
    """ Generate simple not random samples"""
    # sample with repeating characters back to back
    # fff....aaa....nnn...
    chars = (('f','a','n'))
    txt = ""
    for char in chars:
        for x in range(250):
            txt+=char
    file = open(DATA_DIR + "/bigfans.txt",'w')
    file.write(txt)
    file.close()
    txt = ""
    #sample with repeating sequence of characters
    # fanfanfan....
    for x in range(250):
        for char in chars:
            txt+=char
    file = open(DATA_DIR + "/onlyfans.txt",'w')
    file.write(txt)
    file.close()

def compressRLE(filename, data):
    # measure the time needed to strictly compress, byte conversion is not included
    tStart = process_time()
    compressorRLE.compress(data)
    tEnd = process_time()
    #save
    rleFile = open(RLE_DIR+'/'+filename+".crle",'wb')
    rleFile.write(compressorRLE.toByte())
    rleFile.close()
    #return time used
    return tEnd-tStart
def compressLZ(filename, data):
    # measure the time needed to strictly compress, byte conversion is not included
    tStart = process_time()
    lzCompressed  = compressorLZ.compress(data)
    tEnd = process_time()
    #save
    lzFile = open(LZ_DIR + '/' +filename+".lz77", 'wb')
    lzFile.write(compressorLZ.tobyte(lzCompressed))
    lzFile.close()
    #return time used
    return tEnd-tStart

def getStats():
    for filename in os.listdir(DATA_DIR):
        size = os.path.getsize(DATA_DIR + '/'+filename)
        stats[filename].append(size)
    for filename in os.listdir(RLE_DIR):
        size = os.path.getsize(RLE_DIR + '/'+filename)
        filename = filename.replace(".crle","")
        stats[filename].append(size)
    for filename in os.listdir(LZ_DIR):
        size = os.path.getsize(LZ_DIR + '/'+filename)
        filename = filename.replace(".lz77","")
        stats[filename].append(size)


if __name__ == "__main__":
    make_clean()
    generateRandomSamples(10)
    generateSimpleSamples()
    for filename in os.listdir(DATA_DIR):
        #add the file as a key of the dictionnary
        stats[filename] = []
        # read and encode data
        file = open(DATA_DIR +'/'+filename,'rb')
        rawdata = bytearray(file.read())
        data = ""
        for octets in rawdata:
            data+=chr(octets)
        file.close()
        # first two columns are for the time used on each file 
        stats[filename].append(compressRLE(filename, data))
        stats[filename].append(compressLZ(filename, data))
    # add for each key the size before and after both compressions
    getStats()
    # save the files in a csv format
    with open('stats.csv', 'w',newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["file name","RLE time ","LZ77 time","original size","RLE size","LZ77 size","rle ratio", "LZ77 ratio"])
        for key, value in stats.items():
            og = value[2]
            rle=value[3]
            lz=value[4]
            writer.writerow([key,value[0],value[1], og,rle,lz,og/rle,og/lz])
    # go have a coffee until this message is shown
    print("DONE")