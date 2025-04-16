from node import distance

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