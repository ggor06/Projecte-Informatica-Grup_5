import math
#Creació de la classe Node
class Node:
    def __init__(self, name, x, y):
        self.name=name
        self.x=int(x)
        self.y=int(y)
        self.neighbors=[] #Llista de nodes

def AddNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    else:
        n1.neighbors.append(n2)
        return True

def distance(n1, n2):
    dist_x=n2.x - n1.x
    dist_y=n2.y - n1.y
    return math.sqrt(dist_x**2 + dist_y**2)

