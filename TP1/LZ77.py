from ctypes import sizeof
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
# this variable is to enable/disable pritns for debugging
verbose = False
def dPrint(*string):
  if(verbose):
    print(string)
class LZ77:
  """
  Une implementation de l'algorithme LZ77
  """
  MAX_WINDOW_SIZE = 127
  MAX_LOOKAHEAD_SIZE = 63

  def __init__(self, lookaheadBuffer =MAX_LOOKAHEAD_SIZE, window=MAX_WINDOW_SIZE):
    self.bufferSize = min(self.MAX_LOOKAHEAD_SIZE, lookaheadBuffer)
    self.windowSize = min(self.MAX_WINDOW_SIZE, window)

  def compress(self, data):
    """
    compression utilisant LZ77 et les parametres definis dans la classe
    data: Les donnees a compresser
    verbose: faire des print en mi chemin (utile pour le debogage)
    """
    maxlength=0
    triplets = []
    i=0
    while i < len(data):
      # definir le dicitonnaire pour l'iteration
      dict = data[i-self.windowSize:i] if i > self.windowSize else data[0:i]
      # definir le buffer
      buffer = data[i:i+self.bufferSize] if i+self.bufferSize < len(data) - 1 else data[i:-1]
      # debug
      dPrint(" dict =", dict)
      dPrint("buffer = ", buffer)
      match = self.findLongestMatch(buffer,dict)
      dPrint("match = ",match) if len(match)>0 else dPrint("N/A")
      # try to extend the match
      if len(match) > 0 :
        length = self.findRepetition(buffer,match, dict)
        triplets.append((dict.find(match),length,data[i+length]))
        maxlength=max(length,maxlength)
        i+=length+1
      else:
        triplets.append((0,0,data[i]))
        i+=1
      dPrint(triplets)
    return triplets
  def findLongestMatch(self, buffer, dict):
    """trouve la plus longue chaine de character qui se trouve dans dict on utilise juste le buffer est pas tout le data"""
    match = buffer
    while match not in dict and len(match)!= 0:
      match = match[:-1]
    return match

  def findRepetition(self,buffer,match, dict):
    """trouve le nombre de fois que match est repete dans buffer (back to back)"""
    repetitionCounter, bIndex = 0,0
    dIndex = 0
    subDict = dict[dict.find(match):]
    dPrint("dIndex: ",dIndex ," bIndex: ",bIndex," ",subDict[0]," ==? ",buffer[bIndex])
    while bIndex< len(buffer) and buffer[bIndex] == subDict[dIndex] :
      repetitionCounter+=1
      bIndex += 1
      dIndex = (dIndex + 1) % len(subDict)
      #dPrint("dIndex: ",dIndex ," bIndex: ",bIndex," ",dict[dIndex]," ==? ",buffer[bIndex])
    dPrint("repetitions:",repetitionCounter)
    return repetitionCounter

  def decompress(self,triplets):
    retval =""
    for triplet in triplets:
      dPrint(triplet)
      index ,length,nextchar = triplet[0],triplet[1],triplet[2]
      dict = retval[- self.windowSize: ] if self.windowSize < len(retval) else retval
      if (index , length) == (0,0):
        retval += nextchar
        continue
      tmpIndex =index
      for x in range(length):
        retval+= dict[tmpIndex]
        tmpIndex += 1
        if tmpIndex == len(dict):
          tmpIndex = index
      retval+= nextchar
      dPrint(retval)
    return retval
  def frombyte(self, ba):
    """takes a bytearray and return the triplets object"""
    triplets = []
    start=0
    # iterate over the bytearray for each triplets
    while start < len(ba):
      index = ba2int(ba[start:start+self.MAX_WINDOW_SIZE.bit_length()])
      start += self.MAX_WINDOW_SIZE.bit_length()
      length = ba2int(ba[start:start + self.MAX_LOOKAHEAD_SIZE.bit_length()])
      start+= self.MAX_LOOKAHEAD_SIZE.bit_length()
      char = chr(ba2int(ba[start:start+8]))
      start+=8
      triplets.append((index,length,char))
    return triplets
  def tobyte(self, triplets):
    """from the triplets returns bytes"""
    arr = bitarray(endian="big")
    for triplet in triplets:
      index  = int2ba(triplet[0],length=self.MAX_WINDOW_SIZE.bit_length())
      taille = int2ba(triplet[1],length=self.MAX_LOOKAHEAD_SIZE.bit_length())
      char   = int2ba(ord(triplet[2]),length=8)
      arr.extend(index)
      arr.extend(taille)
      arr.extend(char)
    return arr.tobytes()
if __name__ == "__main__":
    print("---------------------------------")
    mystr = "CBAAAAAAAAAAAAAAAAAAAAABAABAACD"
    print(mystr)
    lz = LZ77(22,6)
    compressed = lz.compress(mystr)
    print("---------------------------------")
    print("compressed = ",compressed)
    print("---------------------------------")
    decompressed = lz.decompress(compressed)
    print("decompressed = ", decompressed)
    if decompressed == mystr:
      print("HOOOOORAY")
    octets = lz.tobyte(compressed)
    mybytes = bitarray()
    mybytes.frombytes(octets)
    print("bytify :: ",octets)
    print("debyted ::",lz.frombyte(mybytes))
