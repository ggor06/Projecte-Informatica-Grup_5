class Graph:
    def __init__(self):
        self.navPoints=[]
        self.navSegments=[]
        self.navAirports=[]
        self.navAirspace=[]

def AddNavPoint(g, n):
    if n in g.navPoints:
        return False
    else:
        g.navPoints.append(n)
        return True