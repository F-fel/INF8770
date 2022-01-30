

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
        retval =""
        for code in self.encoding:
            char = code[0]
            count = code[1]
            for x in range(count):
                retval += char
        return retval
    
    def toByte(self):
        """transform the account into a bytes ready to be written"""
        arr = bitarray(endian = "big")
        for duet in self.encoding:
            arr.extend(int2ba(ord(duet[0]),length=8))
            arr.extend(int2ba(duet[1],length=8))
        return arr.tobytes()
    def frombyte(self,ba):
        self.encoding = []
        start =0
        while start<len(ba):
            char = chr(ba2int(ba[start:start+8]))
            count = ba2int(ba[start+8:start+16])
            start+=16
            self.encoding.append((char,count))

if __name__ == "__main__":
    code = "ASSSDEEEGHHGGGTYYY"
    rle = RLE()
    rle.compress(code)
    compressed = rle.toByte()
    print("encoding",rle.encoding)
    print("compressed",compressed)
    print("decoded", rle.decompress())
    ba = bitarray()
    ba.frombytes(compressed)
    rle.frombyte(ba)
    print("decompress from bytes",rle.decompress())
