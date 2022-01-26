tailleDict = 4 # NUMBER OF CHAR IN MEMORY
def encode(message):
    triplets = []  # Pour sauvegarder les triplets
    index = 0  # Position courante dans le message
    while index < len(message):
        decalage = 0
        symbDict = message[max(0, index - tailleDict): index]  # Symboles disponibles du dictionnaire
        if len(symbDict) < tailleDict:
          decalage = tailleDict - len(symbDict) #Pour l'ajustement des indices de position quand le dictionnaire n'est pas plein.
        print(symbDict)
        sousChaine = message[index:len(message)-1] #Le dernier caractère sera ajouté comme 3e élément du dernier triplet

        # On cherche la sous-chaine la plus longue
        pos, length = 0, 0
        while len(sousChaine) > 0:
            if sousChaine in symbDict:
                pos, length = symbDict.rfind(sousChaine), len(sousChaine) #dernière occurrence si plusieurs choix
                break
            sousChaine = sousChaine[:-1] # On a pas trouvé, donc on enlève un élément.

        # Regarde ensuite si on peut allonger la sous-chaine trouvée après la position de l'index: AB|ABABABABAB
        increment = 0
        while length > 0 \
                and index+length+increment < (len(message)-1) \
                and message[index-len(symbDict)+pos+length+increment] == message[index+length+increment]:
            increment += 1
        length += increment

        # Enregistrement des triplets
        c = message[index + length]  #Caractère suivant non encodé.

        if length == 0:
          pos = 0
        else:
          pos = pos + decalage #Pour l'ajustement des indices de position quand le dictionnaire n'est pas plein.

        triplets.append((pos, length, c))

        index += max(length+1, 1)  # Avance la position dans le message

        print(triplets)

        

if __name__ == "__main__":
    str = "ABBACDAABAABAABCDA"
    encode(str)


##  
##  index = 0  # Position courante dans le message
##  while index < len(message):
##      decalage = 0
##      symbDict = message[max(0, index - tailleDict): index]  # Symboles disponibles du dictionnaire
##      if len(symbDict) < tailleDict: 
##        decalage = tailleDict - len(symbDict)#Pour l'ajustement des indices de position quand le dictionnaire n'est pas plein.
##      print(symbDict)
##      sousChaine = message[index:len(message)-1] #Le dernier caractère sera ajouté comme 3e élément du dernier triplet
##  
##      # On cherche la sous-chaine la plus longue
##      pos, length = 0, 0
##      while len(sousChaine) > 0:
##          if sousChaine in symbDict:
##              pos, length = symbDict.rfind(sousChaine), len(sousChaine) #dernière occurrence si plusieurs choix
##              break
##          sousChaine = sousChaine[:-1] # On a pas trouvé, donc on enlève un élément.
##       
##      # Regarde ensuite si on peut allonger la sous-chaine trouvée après la position de l'index: AB|ABABABABAB
##      increment = 0
##      print(triplets)