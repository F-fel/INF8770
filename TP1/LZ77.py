# this variable is to enable/disable pritns for debugging
verbose = False
def dPrint(*string):
  if(verbose):
    print(string)
class LZ77:
  """
  Une implementation de l'algorithme LZ77
  """
  MAX_WINDOW_SIZE = 511
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
  def stringify(self, triplets):
    """to be able to save triplets in a file without the overhead"""
    retval = ""
    for triplet in triplets:
      for x in triplet:
        retval+= str(x)+','
    #remove last comma
    return retval[:-1]
  def deStringify(self, string):
    arr = string.split(',')
    triplets =[]
    for x in range (0,len(arr), 3):
      triplets.append((str(arr[0]),str(arr[1]),arr[2]))
    return triplets


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
      chaine = lz.stringify(compressed)
    print("Stringified : " , chaine)
    print("Destringified : ", lz.deStringify(chaine))