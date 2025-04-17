import math
#Creació de la classe Node
class Node:
    def __init__(self, name, x, y):
        self.name=name
        self.x=int(x)
        self.y=int(y)
        self.neighbors=[] #Llista de nodes
        
# Funció per afegir un veí (n2) a un node (n1)
def AddNeighbor(n1, n2):
    if n2 in n1.neighbors: # Comprovem si n2 ja és veí de n1
        return False        # Si ja hi és, no l'afegim i retornem False
    else:
        n1.neighbors.append(n2) # Si no hi és, l'afegim a la llista de veïns
        return True              # I retornem True per indicar que s'ha afegit
    
# Funció per calcular la distància entre dos nodes (distància euclidiana)
def distance(n1, n2):
    dist_x=n2.x - n1.x
    dist_y=n2.y - n1.y
    return math.sqrt(dist_x**2 + dist_y**2)


