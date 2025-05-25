import math
class navPoint:
    def navPoint(self, code, name, lat, lon):
        self.code=code
        self.name=name
        self.lat=lat
        self.lon=lon
        self.neighbors=[]

def AddNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    else:
        n1.neighbors.append(n2)
        return True

def distance(navP1, navP2):
    dist_x=navP1.lat - navP2.lat
    dist_y=navP1.lon - navP2.lon
    return math.sqrt(dist_x**2 + dist_y**2)