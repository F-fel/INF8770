"""
This is the driver for our project
"""
import csv
import os
import random
from generator import Generator
from RLE import RLE
from LZ77 import LZ77
MIN_SIZE = 1024
MAX = 5120
DATA_DIR = "DATA"
LZ_DIR = "LZ77"
RLE_DIR = "RLE"
sampleFactory = Generator(255)
# compressors
compressorRLE = RLE()
compressorLZ  = LZ77()
# generate samples with random text and size between MIN_SIZE and max bytes
def generateRandomSamples(nSamples):
    for x in range(nSamples):
        length = random.randint(MIN_SIZE,MAX)
        txt = sampleFactory.generate(length)
        file = open(DATA_DIR + "/sample"+str(x), "w")
        file.write(txt)
        file.close()
def generateSimpleSamples():
    # sample with repeating characters back to back
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
    for x in range(250):
        for char in chars:
            txt+=char
    file = open(DATA_DIR + "/onlyfans.txt",'w')
    file.write(txt)
    file.close()

def compress():
    for filename in os.listdir(DATA_DIR):
        # read and encode data
        file = open(DATA_DIR +'/'+filename,'rb')
        rawdata = bytearray(file.read())
        data = ""
        for octets in rawdata:
            data+=chr(octets)
        #compress the data
        lzCompressed  = compressorLZ.compress(data)
        compressorRLE.compress(data)
        file.close()
        #save RLE
        rleFile = open(RLE_DIR+'/'+filename,'wb')
        rleFile.write(compressorRLE.toByte())
        rleFile.close()
        #save LZ77
        lzFile = open(LZ_DIR + '/' +filename+".lz77", 'wb')
        lzFile.write(compressorLZ.tobyte(lzCompressed))
        lzFile.close()
def getStats():
    stats = {}
    for filename in os.listdir(DATA_DIR):
        stats[filename] = []
        size = os.path.getsize(DATA_DIR + '/'+filename)
        stats[filename].append(size)
    for filename in os.listdir(RLE_DIR):
        size = os.path.getsize(RLE_DIR + '/'+filename)
        #filename = filename.replace(".crle","")
        stats[filename].append(size)
    for filename in os.listdir(LZ_DIR):
        size = os.path.getsize(LZ_DIR + '/'+filename)
        filename = filename.replace(".lz77","")
        stats[filename].append(size)
    with open('stats.csv', 'w',newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["file name","original value","RLE value","LZ77 value","rle ratio", "LZ77 ratio"])
        for key, value in stats.items():
            og = value[0]
            rle=value[1]
            lz=value[2]
            writer.writerow([key, og,rle,lz,og/rle,og/lz])

if __name__ == "__main__":
    generateRandomSamples(10)
    generateSimpleSamples()
    compress()
    getStats()
    print("DONE")