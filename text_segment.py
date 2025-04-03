from segment import Segment
from node import Node

n1=Node("Camí antic de valència", 0, 1)
n2=Node("Via Laietana", 5, 6)
n3=Node("Rambla del poblenou", 10, 6)

s1=Segment("Segment1", n1, n2)
s2=Segment("Segment2", n2, n3)

print(round(s1.cost, 1), s2.cost)
