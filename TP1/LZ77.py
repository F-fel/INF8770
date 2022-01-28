import math
from pickle import FALSE
class LZ77:
  """
  Une implementation de l'algorithme LZ77
  """
  MAX_WINDOW_SIZE = 511
  MAX_LOOKAHEAD_SIZE = 63

  def __init__(self, lookaheadBuffer =15, window=20):
    self.bufferSize = min(self.MAX_LOOKAHEAD_SIZE, lookaheadBuffer)
    self.windowSize = min(self.MAX_WINDOW_SIZE, window)

  def compress(self, data, verbose=False):
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
      if verbose : print(" dict =", dict)
      #definir le buffer
      buffer = data[i:i+self.bufferSize] if i+self.bufferSize < len(data) - 1 else data[i:-1]
      if verbose: print("buffer = ", buffer)
      match = self.findLongestMatch(buffer,dict)
      if verbose:
         print(match) if len(match)>0 else print("N/A")
      if len(match) > 0 :
        length = self.findRepetition(buffer,match) * len(match)
        triplets.append((dict.find(match),length,data[i+length]))
        i+=length+1
      else:
        triplets.append((0,0,data[i]))
        i+=1
      if verbose : print(triplets)
    return triplets
  def findLongestMatch(self, buffer, dict):
    """trouve la plus longue chaine de character qui se trouve dans dict on utilise juste le buffer est pas tout le data"""
    match = buffer
    while match not in dict and len(match)!= 0:
      match = match[:-1]
    return match

  def findRepetition(self,buffer,match):
    """trouve le nombre de fois que match est repete dans buffer (back to back)"""
    startIndex = len(match)
    prediction = len(match)
    repetitionCounter =1
    while prediction < len(buffer) \
      and buffer.find(match, startIndex ) == prediction:
      prediction += len(match)
      startIndex += len(match)
      repetitionCounter +=1
    return repetitionCounter
  def decompress(self,triplets):
    retval =""
    for triplet in triplets:
      index ,length,nextchar = triplet[0],triplet[1],triplet[2]
      dict = retval[- self.windowSize: ] if self.windowSize < len(retval) else retval
      if (index , length) == (0,0):
        retval += nextchar
      else:
        a =0


if __name__ == "__main__":
    str = "CBAAAAAAAAAAAAAAAAAAAAABAABAACD"
    lz = LZ77(22,6)
    print(lz.compress(str, verbose=True))