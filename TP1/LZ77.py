from ctypes import sizeof
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
# this variable is to enable/disable prints for manual quick debugging
VERBOSE = False
def dPrint(*string):
  if(VERBOSE):
    print(string)
class LZ77:
  """
  Une implementation de l'algorithme LZ77
  """
  # MAX SIZE OF DICTIONNARY AND BUFFER 
  MAX_WINDOW_SIZE = 127
  MAX_LOOKAHEAD_SIZE = 63 # ALSO SIZE OF LONGEST POSSIBLE MATCH

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
      match = self.findLongestMatch(buffer,dict)
      dPrint(" dict =", dict)
      dPrint("buffer = ", buffer)
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
    """trouve la plus longue chaine de character qui se trouve dans dict on utilise juste le buffer et pas tout le data"""
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
      #EXTRACT DATA FROM TRIPLETS
      index ,length, nextchar = triplet[0],triplet[1],triplet[2]
      # reconstruct dictionnary
      dict = retval[- self.windowSize: ] if self.windowSize < len(retval) else retval
      # if new char skip the rest
      if (index , length) == (0,0):
        retval += nextchar
        continue
      #reconstruct string from dictionnary
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
    index_length = self.MAX_WINDOW_SIZE.bit_length()
    dPrint("index length", index_length)
    buffer_length = self.MAX_LOOKAHEAD_SIZE.bit_length()
    dPrint("index length", buffer_length)
    dPrint("len(ba) : ", len(ba))
    while start < (len(ba) - 21):
    # iterate over the bytearray for each triplets
      #extract the amount of bits needed for each metric
      dPrint("start: ",start )
      index = ba2int(ba[start:start+index_length])
      start += index_length
      length = ba2int(ba[start:start + buffer_length])
      start+= buffer_length
      char = chr(ba2int(ba[start:start+8]))
      start+=8
      triplets.append((index,length,char))
    return triplets
  def tobyte(self, triplets):
    """from the triplets returns bytes"""
    arr = bitarray(endian="big")
    for triplet in triplets:
      # convert data into a bit array with the correct size
      index  = int2ba(triplet[0],length=self.MAX_WINDOW_SIZE.bit_length())
      taille = int2ba(triplet[1],length=self.MAX_LOOKAHEAD_SIZE.bit_length())
      char   = int2ba(ord(triplet[2]),length=8)
      arr.extend(index)
      arr.extend(taille)
      arr.extend(char)
    return arr.tobytes()

if __name__ == "__main__":
    print("------------------------- initial string -----------------------------")
    mystr = "CBAAAAAAAAAAAAAAAAAAAAABAABAACD"
    print(mystr)
    lz = LZ77(22,6)
    compressed = lz.compress(mystr)
    print("\n--------------compression and decompression results -------------------\n")
    print("compressed = ",compressed)
    decompressed = lz.decompress(compressed)
    print("decompressed = ", decompressed)
    print("-----------------------------------------------------------------------")
    print("NO DATA LOST TEST : ", decompressed == mystr)
    print("\n-------------------RESULTS WITH BIT MANIPULATION-----------------------\n")
    octets = lz.tobyte(compressed)
    mybytes = bitarray()
    mybytes.frombytes(octets)
    byteresults = lz.frombyte(mybytes)
    print("bytify :: ",octets)
    print(mybytes)
    print("debyted ::",byteresults)
    print("----------------------------------------------------------------------")
    print("NO DATA LOST TEST AFTER BIT MANIPULATION : ", byteresults == compressed )