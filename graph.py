import math
import matplotlib.pyplot as plt
from segment import Segment
from node import AddNeighbor, Node
import tkinter as tk
#Creació de la classe Graph
class Graph:
    def __init__(self):
        self.nodes=[]   # Llista de nodes del graf
        self.segments=[]     # Llista de segments (connexions) entre nodes


# Afegeix un node al graf, si no hi és ja
def AddNode(g, n):
    if n in g.nodes:
        return False
    else:
        g.nodes.append(n)
        return True

'''l
def AddSegment(g, nameOriginNode, nameDestinationNode):
    if nameOriginNode or nameDestinationNode not in g.nodes[0]:
        return False
    else:
        g.segments.append(Segment("Segment", nameOriginNode, nameDestinationNode))
        AddNeighbor(nameOriginNode, nameDestinationNode)
        return True
'''
#La versió aquesta té un error, de comprovar si els noms dels nodes existeixen al graf. 
#L'operador or que fem servir no és adequat per aquest cas. 
# La condició if nameOriginNode or nameDestinationNode not in g.nodes[0]: no funciona bé, ja que s'està comprovant si nameOriginNode és cert 
# (no None, no una cadena buida, etc.), i després fa la comparació incorrecta per a nameDestinationNode.

#Versió corregida per GPT
def AddSegment(g, nameOriginNode, nameDestinationNode, segmentName=None):
    # Busca els nodes pel seu nom
    origin_node = None
    destination_node = None

    for node in g.nodes:
        if node.name == nameOriginNode:
            origin_node = node
        if node.name == nameDestinationNode:
            destination_node = node

    # Si algun no s'ha trobat, sortim
    if origin_node is None or destination_node is None:
        return False

    # Si no ens han passat el nom, en creem un automàticament
    if segmentName is None:
        segmentName = f"Segment_{nameOriginNode}_{nameDestinationNode}"

    # Crear i afegir el segment
    new_segment = Segment(segmentName, origin_node, destination_node)
    g.segments.append(new_segment)

    # Afegim veí
    AddNeighbor(origin_node, destination_node)

    return True


# Llegeix els nodes del fitxer "Nodes.txt"
def ReadNode(g):
    try:
        with open("Nodes.txt", "r") as F:  # Obrim el fitxer en mode lectura
            linea = F.readline() 
            while linea != "":
                elementos = linea.split()  
                if len(elementos) == 3: 
                    nom = elementos[0]
                    x = float(elementos[1]) 
                    y = float(elementos[2])  
                    g.nodes.append(Node(nom, x, y))  
                linea = F.readline()  
    except FileNotFoundError:
        print("ERROR: No es pot obrir el fitxer 'Nodes.txt'.")
    except Exception as e:
        print(f"ERROR: {e}")
    F.close()
    
def ReadSegment():
    try:
        with open("Segment", "r") as F:
            linea = F.readline()
    except FileNotFoundError:
        print("ERROR: No es pot obrir el fitxer 'Nodes.txt'.")
    except Exception as e:
        print(f"ERROR: {e}")
        
# Troba el node més proper a unes coordenades (x, y)
def GetClosest(g, x, y):
    closest_node=None   # Inicialitzem el node més proper com a None
    min_distance=float('inf') #És un número molt gran
    for n in g.nodes:
        d=math.sqrt((n.x-x)**2+(n.y-y)**2)
        if d < min_distance:
            min_distance=d  # Si la nova distància és més petita, l’actualitzem
            closest_node=n  # I també el node més proper
    
    return closest_node # Retornem el node més proper
# Per suggerencia de GPT hem canviat plt.text per a un que sigui ax.text, així quan en la funció es cridada per un altra per posarla en la UI no crea un altre plot sinó que surt en la UI
# Visualitza el graf complet (nodes i segments)
def Plot(g, ax):
    #llista de nodes
    for node in g.nodes:
        ax.plot(node.x, node.y, 'o', color='red', markersize=5)    # Dibuixem el node com un punt vermell
        ax.text(node.x + 0.5, node.y + 0.5, node.name, color='black', weight='bold', fontsize=6)   # Etiqueta amb el nom
    #llista de segments
    for segment in g.segments:
        ax.plot([segment.o_node.x, segment.d_node.x], [segment.o_node.y, segment.d_node.y], color='blue', linewidth=1) # Dibuixem la línia entre nodes

    #Punt mig
    for segment in g.segments:
        mid_x=(segment.o_node.x+segment.d_node.x)/2
        mid_y=(segment.o_node.y+segment.d_node.y)/2
        ax.text(mid_x, mid_y, segment.cost, color='purple', fontsize=5)

def PlotNode(g, nameOrigin, ax):
    
    # Busquem el node amb el nom donat i si no el troba et retorna false
    for node in g.nodes:
        ax.plot(node.x, node.y, 'o', color='gray', markersize=5)
        
    origin_node = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin_node = node
            break
    if origin_node is None:
        return False

    ax.plot(origin_node.x, origin_node.y, 'o', color='blue', markersize=5)
    
    for neighbor in origin_node.neighbors:
        ax.plot(neighbor.x, neighbor.y, 'o', color='green', markersize=5)
        
    for other_node in g.nodes:
        if other_node != origin_node and other_node not in origin_node.neighbors:
            ax.plot(other_node.x, other_node.y, 'o', color='gray', markersize=5)

    # Dibuixa els segments
    for segment in g.segments:
        if segment.o_node == origin_node:
            ax.arrow(segment.o_node.x, segment.o_node.y, 
                      segment.d_node.x - segment.o_node.x, segment.d_node.y - segment.o_node.y,
                      head_width=0.5, head_length=0.5, fc="blue", ec="blue")
    return True

def CreateGraph_1():
    G = Graph() 

    # Afegim els nodes
    
    ReadNode(G)
    AddSegment(G, "A", "B")
    AddSegment(G, "A", "E")
    AddSegment(G, "A", "K")
    AddSegment(G, "B", "A")
    AddSegment(G, "B", "C")
    AddSegment(G, "B", "F")
    AddSegment(G, "B", "K")
    AddSegment(G, "B", "G")
    AddSegment(G, "C", "D")
    AddSegment(G, "C", "G")
    AddSegment(G, "D", "G")
    AddSegment(G, "D", "H")
    AddSegment(G, "D", "I")
    AddSegment(G, "E", "F")
    AddSegment(G, "F", "L")
    AddSegment(G, "G", "B")
    AddSegment(G, "G", "F")
    AddSegment(G, "G", "H")
    AddSegment(G, "I", "D")
    AddSegment(G, "I", "J")
    AddSegment(G, "J", "I")
    AddSegment(G, "K", "A")
    AddSegment(G, "K", "L")
    AddSegment(G, "L", "K")
    AddSegment(G, "L", "F")
    return G

def LecturaNodos(g, datos, ax, canvas):
    vec=datos.split(" ")
    node = Node(vec[0], float(vec[1]), float(vec[2]))
    g.nodes.append(node)
    with open("saved_nodes.txt", "a") as F:
        F.write(datos.strip() + '\n')
    #Redibuix del canvas
    ax.clear()
    Plot(g, ax)
    canvas.draw()

def LecturaSegmentos(g, datos, ax, canvas):
    vec=datos.split(" ")
    origin_node = None
    destiny_node=None
    for node in g.nodes:
        if node.name == vec[1]:
            origin_node = node
            break
    if origin_node is None:
        return False
    for node in g.nodes:
        if node.name == vec[2]:
            destiny_node=node
            break
    if destiny_node is None:
        return False
    segment = Segment(vec[0], origin_node, destiny_node)
    g.segments.append(segment)
    with open("saved_segments.txt", "a") as F:
        F.write(datos.strip() + '\n')
    #Redibuix del canvas
    ax.clear()
    Plot(g, ax)
    canvas.draw()

def RemoveNode(g, name):
    node_to_remove = None
    for node in g.nodes:
        if node.name == name:
            node_to_remove = node
            break
    if node_to_remove is None:
        return False
    g.nodes.remove(node_to_remove)
    g.segments = [s for s in g.segments if s.o_node != node_to_remove and s.d_node != node_to_remove]
    for node in g.nodes:
        if node_to_remove in node.neighbors:
            node.neighbors.remove(node_to_remove)
    #Aportació de IA
    # ✅ Actualitzar fitxer saved_nodes.txt
    with open("saved_nodes.txt", "w") as f:
        for node in g.nodes:
            f.write(f"{node.name} {node.x} {node.y}\n")

    # ✅ Actualitzar fitxer saved_segments.txt
    with open("saved_segments.txt", "w") as f:
        for seg in g.segments:
            f.write(f"{seg.name} {seg.o_node.name} {seg.d_node.name}\n")

    return True


def LoadSavedNodes(g, path):
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 3:
                    name, x, y = parts
                    node = Node(name, float(x), float(y))
                    AddNode(g, node)
    except FileNotFoundError:
        print(f"No hay el rchivo {path}")

def LoadSavedSegments(g, path):
    try:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    name, origin, dest = parts[:3]
                    AddSegment(g, origin, dest, name)
    except FileNotFoundError:
        print(f"No s'ha trobat el fitxer {path}")
