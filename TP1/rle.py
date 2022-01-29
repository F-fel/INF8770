from itsdangerous import encoding
from markupsafe import string


class RLE:
    def __init__(self):
        pass
    #Ce code est adapte de GeeksforGeeks, https://www.geeksforgeeks.org/run-length-encoding/
    def encode(self, data):
        encoding = []
        n = len(data)
        i = 0
        while i < n- 1:
        
            # Count occurrences of
            # current character
            count = 1
            while (i < n - 1 and
                   data[i] == data[i + 1]):
                count += 1
                i += 1
            i += 1
            encoding.append((data[i-1], str(count)))
        return encoding
    def decode(self, encoding):
        retval =""
        for code in encoding:
            char = encoding[0]
            count = encoding[1]
            for x in range(count):
                retval += char
        return retval
    def stringify(self, encoding):
        retval = ""
        for duet in encoding:
            retval += duet[0]+','+duet[1]+','
        return retval[:-1]
    def deString(self,string):
        encoding = []
        splitString = string.split(',')
        for x in range(0,len(splitString),2):
            encoding.append((splitString[x],splitString[x+1]))
if __name__ == "__main__":
    code = "ASSSDEEEGHHGGGTYYY"
    rle = RLE()
    encoding = rle.encode(code)
    print(rle.stringify(encoding))
