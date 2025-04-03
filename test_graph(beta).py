from graph import AddNode, AddNeighbor, AddSegment, Plot, GetClosest, Graph, PlotNode, ReadNode
from segment import Segment
from node import Node, AddNeighbor, distance
import matplotlib.pyplot as plt

def CreateGraph_1():
    G = Graph()  # Creem el graf correctament
    print("📌 Creant nodes...")

    # Afegim els nodes
    ReadNode()

    print("📌 Nodes afegits:", [n.name for n in G.nodes])

    # Afegim els segments (ara correctament)
    print("📌 Afegint segments...")
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

    print("📌 Segments afegits:", [(s.o_node.name, s.d_node.name) for s in G.segments])

    return G  # Tornem el graf correctament

# Prova del graf
print("🔄 Probant el graf...")
G = CreateGraph_1()

Plot(G)
PlotNode(G, "C")

# Prova de GetClosest
n = GetClosest(G, 15, 5)
print("📌 Node més proper a (15,5):", n.name)  # Ha de ser J

n = GetClosest(G, 8, 19)
print("📌 Node més proper a (8,19):", n.name)  # Ha de ser B
