from bitarray import bitarray
from bitarray.util import int2ba, ba2int

class RLE:
    MAX_REPETITION = 255
    def __init__(self):
        self.encoding = []
    def compress(self, data):
        #Ce code est adapte de GeeksforGeeks, https://www.geeksforgeeks.org/run-length-encoding/
        self.encoding = []
        n = len(data)
        i = 0
        while i < n- 1:
        
            # Count occurrences of
            # current character
            count = 1
            while (i < n - 1 and
                   data[i] == data[i + 1] and count < self.MAX_REPETITION):
                count += 1
                i += 1
            i += 1
            self.encoding.append((data[i-1], count))
        return self.encoding

    def decompress(self):
        #pretty self explanatory 
        retval =""
        for code in self.encoding:
            char = code[0]
            count = code[1]
            for x in range(count):
                retval += char
        return retval
    
    def toByte(self):
        """transform the account into bytes ready to be written in files"""
        arr = bitarray(endian = "big")
        for duet in self.encoding:
            arr.extend(int2ba(ord(duet[0]),length=8))
            arr.extend(int2ba(duet[1],length=8))
        return arr.tobytes()
    def frombyte(self,ba):
        '''converts a byte array into a 2d array '''
        self.encoding = []
        start =0
        while start<len(ba):
            char = chr(ba2int(ba[start:start+8]))
            count = ba2int(ba[start+8:start+16])
            start+=16
            self.encoding.append((char,count))

if __name__ == "__main__":
    #initialis token, feel free to test with another string
    token = "ASSSDEEEGHHGGGTYYY"
    rle = RLE()
    ba = bitarray()
    # compress and decompress to check algorithm, to decompress another token you can set rle.encoding to the array 
    rle.compress(token)
    decoded = rle.decompress()
    #<-- manual testing + no data loss confirmation -->
    print("encoding",rle.encoding)
    print("decoded", decoded)
    print("NO DATA LOST : ", (decoded == token))
    #<--- bit manipulation section : --->
    compressed = rle.toByte()
    # this is not worth writing a test , so check manually
    print("compressed",compressed)
    ba.frombytes(compressed)
    rle.frombyte(ba)
    print("No data lost in bits : ", (token == rle.decompress()))
    print("decompress from bytes",rle.decompress())
