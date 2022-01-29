"""
This is the driver for our project
"""
import os
import random
from generator import Generator
from RLE import RLE
from LZ77 import LZ77
MIN = 1024
MAX = 5120
SAMPLE_SIZE = 60
DATA_DIR = "DATA"
LZ_DIR = "LZ77"
RLE_DIR = "RLE"
# assuming we read files as hexadecimals
sampleFactory = Generator(16)
# compressors
compressorRLE = RLE()
compressorLZ  = LZ77()
# generate samples of length in  [min;max]
for x in range(SAMPLE_SIZE):
    length = random.randint(MIN,MAX)
    txt = sampleFactory.generate(length)
    file = open(DATA_DIR + "/sample"+str(x), "w")
    file.write(txt)
    file.close()

for filename in os.listdir(DATA_DIR):
    # read and encode data
    file = open(DATA_DIR +'/'+filename,'r')
    data = file.read()
    rleCompressed = compressorRLE.encode(data)
    lzCompressed  = compressorLZ.compress(data)
    file.close()
    #save RLE
    rleFile = open(RLE_DIR+'/'+filename,'w')
    rleFile.write(compressorRLE.stringify(rleCompressed))
    rleFile.close()
    #save LZ77
    lzFile = open(LZ_DIR + '/' +filename, 'w')
    lzFile.write(compressorLZ.stringify(lzCompressed))
    lzFile.close()

    