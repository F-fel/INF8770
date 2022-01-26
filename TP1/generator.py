import random
import string
class Generator:
    def __init__(self, size,nchars):
        self.size=size
        self.nchars=nchars
        self.txt = ""
    def generate(self,length):
        for x in range (length):
            self.txt +=random.choice(string.ascii_letters[0:self.nchars])
    def save(self,path):
        file = open(path,"w")
        file.write(self.str)
