from navPoint import distance
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt

class Path:
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes else []
        self.real_cost = 0
        self.co2=0

    def last_node(self):
        return self.nodes[-1] if self.nodes else None

    def estimated_total_cost(self, destination):
        if not self.nodes:
            return float('inf')
        last = self.last_node()
        return self.real_cost + distance(last, destination)

    def copy_and_add(self, node):
        new_path = Path(self.nodes + [node])
        new_path.real_cost = self.real_cost + distance(self.last_node(), node)
        return new_path

def AddNode2Path(path, node):
    if node in path.nodes:
        print("Ja està en la llista")
        return False
    if path.nodes:
        path.real_cost += distance(path.nodes[-1], node)
    path.nodes.append(node)
    return True

def ContainsNode(path, node):
    return node in path.nodes

def Cost2Node(path, node):
    if node not in path.nodes:
        return -1
    cost = 0
    for i in range(1, path.nodes.index(node) + 1):
        cost += distance(path.nodes[i - 1], path.nodes[i])
    return cost

def PlotPath(g, path, ax):
    path.real_cost=0
    # nodes del camí
    for node in path.nodes:
        ax.plot(node.lon, node.lat, "o", color="red", markersize=5)

    # fletxes del camí
    for n1, n2 in zip(path.nodes[:-1], path.nodes[1:]):
        arrow = FancyArrowPatch((n1.lon, n1.lat), (n2.lon, n2.lat), arrowstyle="->", color="blue", mutation_scale=10, linewidth=1,)
        ax.add_patch(arrow)
        seg_cost = distance(n1, n2)
        path.real_cost += seg_cost
        path._co2_computed = True

    # resta de nodes del graf
    for node in g.navPoints:
        ax.plot(node.lon, node.lat, "o", color="gray", markersize=5)
        ax.text(node.lon + 0.3, node.lat + 0.3, node.name, fontsize=8)
    
    #Factor d'emissions
    factor=9.2 
    path.co2=factor*path.real_cost
    # ajustos d’eix
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.relim()
    ax.autoscale_view()

def txtGen(path, filename="Resultat.txt"):
    if not getattr(path, "_co2_computed", False):
        print("Error: abans has de cridar PlotPath(g, path, ax) per calcular la petjada de CO₂.")
        return

    try:
        with open(filename, 'w') as f:
            for node in path.nodes:
                dist = Cost2Node(path, node)
                co2 = 9.2 * dist
                f.write(f"{node.code} {node.name} {co2:.2f} kg\n")
    except Exception as e:
        print(f"Error generant '{filename}': {e}")