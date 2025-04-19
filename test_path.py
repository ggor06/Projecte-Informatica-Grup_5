from path import Path, AddNode2Path, Cost2Node, ContainsNode, PlotPath
from node import Node
from graph import Graph, AddSegment
import matplotlib.pyplot as plt

# Crear alguns nodes de prova
n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)

# Crear un camí buit
path = Path()

# Test AddNodeToPath
print("Afegint A:", AddNode2Path(path, n1))  # Esperat: True
print("Afegint B:", AddNode2Path(path, n2))  # Esperat: True
print("Reafegint A:", AddNode2Path(path, n1))  # Esperat: False

# Test ContainsNode
print("Conté A?", ContainsNode(path, n1))  # Esperat: True
print("Conté C?", ContainsNode(path, n3))  # Esperat: False

# Test CostToNode
print("Cost fins a A:", Cost2Node(path, n1))  # Esperat: 0
print("Cost fins a B:", Cost2Node(path, n2))  # Esperat: distància AB = 5.0
print("Cost fins a C:", Cost2Node(path, n3))  # Esperat: -1

# Test PlotPath
AddNode2Path(path, n3)
G = Graph()
G.nodes.extend([n1, n2, n3])
AddSegment(G, "A", "B")
AddSegment(G, "B", "C")

fig, ax = plt.subplots()
PlotPath(G, path, ax)
ax.set_title("Test de PlotPath")
plt.show()

