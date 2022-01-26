class RLE:
    def __init__(self):
        print("TODO: constuctor RLE")
    #Ce code est adapte de GeeksforGeeks, https://www.geeksforgeeks.org/run-length-encoding/
    def encode(self, data):
        encoding = ""
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
        encoding = data[i-1] + str(count)
    
