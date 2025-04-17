from node import distance
from segment import Segment

class Path:
    def __init__(self, nodes=None):
        self.nodes = nodes if nodes else []
        self.real_cost = 0  # Cost real acumulat

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
    else:
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
    i = 1
    while i <= path.nodes.index(node):
        cost += distance(path.nodes[i - 1], path.nodes[i])
        i += 1
    return cost

def PlotPath(g, path, ax):
    for node in path.nodes:
        ax.plot(node.x, node.y, 'o', color='red', markersize=5)
    i = 0
    while i < len(path.nodes) - 1:
        n1 = path.nodes[i]
        n2 = path.nodes[i + 1]
        ax.arrow(n1.x, n1.y, n2.x - n1.x, n2.y - n1.y, head_width=0.5, head_length=0.5, fc="blue", ec="blue")
        i += 1
    
