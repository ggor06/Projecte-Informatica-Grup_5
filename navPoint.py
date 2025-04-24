import math
class navPoint:
    def navPoint(self, code, name, lat, lon):
        self.code=code
        self.name=name
        self.lat=lat
        self.lon=lon
        self.neighbors=[]

# Funció per afegir un veí (n2) a un navPoint (n1)
def AddNeighbor(n1, n2):
    if n2 in n1.neighbors: # Comprovem si n2 ja és veí de n1
        return False        # Si ja hi és, no l'afegim i retornem False
    else:
        n1.neighbors.append(n2) # Si no hi és, l'afegim a la llista de veïns
        return True              # I retornem True per indicar que s'ha afegit

def distance(navP1, navP2):
    dist_x=navP1.lat - navP2.lat
    dist_y=navP1.lon - navP2.lon
    return math.sqrt(dist_x**2 + dist_y**2)