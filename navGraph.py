from navSegment import navSegment
from navPoint import navPoint, AddNeighbor, distance
import math
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

class Graph:
    def __init__(self):
        self.navPoints=[]
        self.navSegments=[]
        self.navAirports=[]
        self.navAirspace=[]

def FindNavPoint(g, identifier):
    key = identifier.strip().lower()
    for np in g.navPoints:
        if np.code.lower() == key or np.name.lower() == key:
            return np
    return None

def FindShortestPathByName(g, origin_id, dest_id):
    ori = FindNavPoint(g, origin_id)
    dst = FindNavPoint(g, dest_id)
    if ori is None or dst is None:
        raise ValueError(f"Waypoint desconegut: {origin_id!r} o {dest_id!r}")
    return FindShortestPath(g, ori.code, dst.code)

def FindAirport(g, airport_name):
    key = airport_name.strip().lower()
    for ap in g.navAirports:
        if ap.name.lower() == key:
            return ap
    return None

def FindShortestPathBetweenAirports(g, origin_air, dest_air):
    a1 = FindAirport(g, origin_air)
    a2 = FindAirport(g, dest_air)
    if not a1 or not a2:
        raise ValueError(f"Aeroport desconegut: {origin_air!r} o {dest_air!r}")

    best_path = None
    best_cost = float('inf')

    for sid in a1.sid:
        for star in a2.star:
            try:
                path = FindShortestPath(g, sid.code, star.code)
            except Exception:
                continue
            if not path:
                continue
            cost = sum(distance(path[i], path[i+1]) for i in range(len(path)-1))
            if cost < best_cost:
                best_cost, best_path = cost, path

    return best_path

#Funció per afegir un navPoint
def AddNavPoint(g, code, name, lat, lon):
    for p in g.navPoints:
        if p.code == code:
            return False  
    p = navPoint()
    p.navPoint(code, name, float(lat), float(lon))
    g.navPoints.append(p)
    return True

#Funció per afegir un segment
def AddSegment(g, originCode, destinationCode):
    origin_node = None
    destination_node = None

    for node in g.navPoints:
        if node.code == originCode:
            origin_node = node
        if node.code == destinationCode:
            destination_node = node

    if origin_node is None or destination_node is None:
        return False

    dist = distance(origin_node, destination_node)

    new_segment = navSegment()
    new_segment.navSegment(originCode, destinationCode, dist)

    g.navSegments.append(new_segment)

    AddNeighbor(origin_node, destination_node)
    return True

#Funció per saber si t'apropes a un lloc
def GetClosest(g, x, y):
    closest_node=None  
    min_distance=float('inf') 
    for n in g.navPoints:
        d=math.sqrt((n.lat-x)**2+(n.lon-y)**2)
        if d < min_distance:
            min_distance=d  
            closest_node=n 
    return closest_node 

#Funció per fer el plot del espai aeri
def Plot(g, ax):

    for node in g.navPoints:
        ax.plot(node.lon, node.lat, 'o', color='red', markersize=5)
        ax.text(node.lon + 0.01, node.lat + 0.01, node.name, fontsize=6, ha='left', va='bottom')

    for segment in g.navSegments:

        o = next(n for n in g.navPoints if n.code == segment.originNumber)
        d = next(n for n in g.navPoints if n.code == segment.destinationNumber)

        ax.plot([o.lon, d.lon], [o.lat, d.lat], color='blue', linewidth=1)

        mid_lon = 0.5 * (o.lon + d.lon)
        mid_lat = 0.5 * (o.lat + d.lat)
        ax.text(mid_lon, mid_lat, f"{segment.distance:.1f}", fontsize=6, ha='center', va='center', color='purple')

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.relim()
    ax.autoscale_view()

#Funció per fer el plot dels veïns
def PlotNode(g, originCode, ax):
    for node in g.navPoints:
        ax.plot(node.lon, node.lat, 'o', color='gray', markersize=5)

    origin = next((n for n in g.navPoints if n.code == originCode), None)
    if origin is None:
        return False

    ax.plot(origin.lon, origin.lat, 'o', color='blue', markersize=5)

    for nb in origin.neighbors:
        ax.plot(nb.lon, nb.lat, 'o', color='green', markersize=5)

    for seg in g.navSegments:
        if seg.originNumber == originCode:
            dest = next(n for n in g.navPoints if n.code == seg.destinationNumber)
            arrow = FancyArrowPatch((origin.lon, origin.lat), (dest.lon,  dest.lat), arrowstyle='->', color='blue', mutation_scale=10, linewidth=1)
            ax.add_patch(arrow)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.relim()
    ax.autoscale_view()

    return True

#Trobar el camí més petit
def FindShortestPath(g, originCode, destinationCode):
    oriNode = None
    destNode = None

    for node in g.navPoints:
        if node.code == originCode:
            oriNode = node
        if node.code == destinationCode:
            destNode = node

    if oriNode is None or destNode is None:
        return None

    cues = [[oriNode]]
    visitats = []

    while len(cues) > 0:
        cami = cues[0]
        cues = cues[1:]
        actual = cami[-1]

        if actual == destNode:
            return cami

        if actual not in visitats:
            visitats.append(actual)
            for vei in actual.neighbors:
                if vei not in visitats:
                    nou_cami = cami + [vei]
                    cues.append(nou_cami)
    return None
    
def createGraph():
    G=Graph()
    return G

#Eliminació d'un navPoint
def RemoveNavPoint(g, code):
    node_to_remove = None
    for node in g.navPoints:
        if node.code == code:
            node_to_remove = node
            break
    if node_to_remove is None:
        return False
    
    g.navPoints.remove(node_to_remove)
    g.navSegments = [s for s in g.navSegments if s.originNumber != code and s.destinationNumber != code]
    for node in g.navPoints:
        if node_to_remove in node.neighbors:
            node.neighbors.remove(node_to_remove)

    SaveNavPoints(g, "navPoints.txt")
    SaveNavSegments(g, "navSegments.txt")
    
    return True

#Funció de lectura de navPoints
def ReadNavPoints(g, file):
    g.navPoints.clear()
    try:
        with open(file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                code, name, lat, lon = parts[0], parts[1], float(parts[2]), float(parts[3])
                AddNavPoint(g, code, name, lat, lon)
    except FileNotFoundError:
        print(f"ERROR: No s'ha trobat el fitxer {file}")
    except Exception as e:
        print(f"ERROR llegint dades del graf: {e}")

#Funció de lectura de segments
def ReadNavSegments(g, file):
    g.navSegments.clear()
    try:
        with open(file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                codeO, codeD, _ = parts[0], parts[1], float(parts[2])
                AddSegment(g, codeO, codeD)
    except FileNotFoundError:
        print(f"ERROR: No s'ha trobat el fitxer {file}")
    except Exception as e:
        print(f"ERROR llegint dades del graf: {e}")

def SaveNavPoints(g, filepath="saved_navPoints.txt"):
    with open(filepath, "w") as f:
        for node in g.navPoints:
            f.write(f"{node.code} {node.name} {node.lat} {node.lon}\n")

def SaveNavSegments(g, filepath="saved_navSegments.txt"):
    with open(filepath, "w") as f:
        for segment in g.navSegments:
            f.write(f"{segment.originNumber} {segment.destinationNumber} {segment.distance}\n" )

#Lectura de la introducció per part del usuari d'un nou navPoint
def LecturaNavPoints(g, datos, ax, canvas):
    vec = datos.split(" ")
    code = vec[0]
    name = vec[1]
    lat = float(vec[3])
    lon = float(vec[2])

    p = navPoint()
    p.navPoint(code, name, lat, lon)
    g.navPoints.append(p)

    SaveNavPoints(g, "navPoints.txt")
    ax.clear()
    Plot(g, ax)
    canvas.draw()

#Lectura de la introducció per part del usuari d'un nou segment
def LecturaNavSegments(g, datos, ax, canvas):
    vec = datos.strip().split()
    if len(vec) < 2:
        return False

    origin_code = vec[0]
    dest_code = vec[1]
    origin_node = None
    dest_node = None
    for node in g.navPoints:
        if node.code == origin_code:
            origin_node = node
        
        if node.code == dest_code:
            dest_node = node

    if origin_node is None or dest_node is None:
        return False

    from navPoint import distance
    dist = distance(origin_node, dest_node)

    s = navSegment()
    s.navSegment(origin_code, dest_code, dist)
    g.navSegments.append(s)

    AddNeighbor(origin_node, dest_node)
    SaveNavSegments(g, "navSegments.txt")
    ax.clear()
    Plot(g, ax)
    canvas.draw()
    return True

__all__ = ["createGraph", "ReadNavPoints", "ReadNavSegments", "SaveNavPoints", "SaveNavSegments","AddNavPoint", "AddSegment", "RemoveNavPoint","Plot", "PlotNode", "FindShortestPath","FindNavPoint", "FindShortestPathByName", "FindAirport", "FindShortestPathBetweenAirports","LecturaNavPoints", "LecturaNavSegments"]
