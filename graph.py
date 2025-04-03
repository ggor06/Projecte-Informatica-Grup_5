import math
import matplotlib.pyplot as plt
from segment import Segment
from node import AddNeighbor, Node
#Creació de la classe Graph
class Graph:
    def __init__(self):
        self.nodes=[]
        self.segments=[]



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
def AddSegment(g, nameOriginNode, nameDestinationNode):
    # Cerca els nodes pel seu nom
    origin_node = None
    destination_node = None

    # Busquem els nodes pel seu nom
    for node in g.nodes:
        if node.name == nameOriginNode:
            origin_node = node
        if node.name == nameDestinationNode:
            destination_node = node

    # Comprova si hem trobat els dos nodes
    if origin_node is None or destination_node is None: 
        return False  

    # Crea i afegeix el segment al graf
    new_segment = Segment(f"Segment_{origin_node.name}_{destination_node.name}", origin_node, destination_node)
    g.segments.append(new_segment)

    # Actualitza la llista de veïns del node d'origen
    AddNeighbor(origin_node, destination_node)

    return True

def ReadNode(g):
    try:
        with open("Nodes.txt", "r") as F:  
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

def GetClosest(g, x, y):
    closest_node=None
    min_distance=float('inf') #És un número molt gran
    for n in g.nodes:
        d=math.sqrt((n.x-x)**2+(n.y-y)**2)
        if d < min_distance:
            min_distance=d
            closest_node=n
    
    return closest_node

def Plot(g):
    #llista de nodes
    for node in g.nodes:
        plt.plot(node.x, node.y, 'o', color='red', markersize=5)
        plt.text(node.x + 0.5, node.y + 0.5, node.name, color='black', weight='bold', fontsize=6)
    #llista de segments
    for segment in g.segments:
        plt.plot([segment.o_node.x, segment.d_node.x], [segment.o_node.y, segment.d_node.y], color='blue', linewidth=1)

    #Punt mig
    for segment in g.segments:
        mid_x=(segment.o_node.x+segment.d_node.x)/2
        mid_y=(segment.o_node.y+segment.d_node.y)/2
        plt.text(mid_x, mid_y, segment.cost, color='purple', fontsize=5)

    plt.show()

def PlotNode(g, nameOrigin):

    # Busquem el node amb el nom donat i si no el troba et retorna false
    origin_node = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin_node = node
            break
    if origin_node is None:
        return False

    plt.plot(origin_node.x, origin_node.y, 'o', color='blue', markersize=5)
    
    for neighbor in origin_node.neighbors:
        plt.plot(neighbor.x, neighbor.y, 'o', color='green', markersize=5)
        
    for other_node in g.nodes:
        if other_node != origin_node and other_node not in origin_node.neighbors:
            plt.plot(other_node.x, other_node.y, 'o', color='gray', markersize=5)

    # Dibuixa els segments
    for segment in g.segments:
        if segment.o_node == origin_node:
            plt.arrow(segment.o_node.x, segment.o_node.y, 
                      segment.d_node.x - segment.o_node.x, segment.d_node.y - segment.o_node.y,
                      head_width=0.5, head_length=0.5, fc="blue", ec="blue")
    plt.show()
    return True


