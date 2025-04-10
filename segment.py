#Creació de la classe Segment
from node import distance
class Segment:
    def __init__(self, name, o_node, d_node):
        self.name=name
        self.o_node=o_node
        self.d_node=d_node
        self.cost=round(distance(o_node, d_node),1)