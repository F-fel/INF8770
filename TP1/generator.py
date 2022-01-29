import random
import string
class Generator:
    def __init__(self, nchars):
        self.nchars=nchars
    def generate(self,length):
        txt =""
        for x in range (length):
            txt +=random.choice(string.ascii_letters[0:self.nchars])
        return txt