from rdflib import Graph
import pprint

g = Graph()
g.parse("sto.ttl", format="turtle")

len(g) # prints 2


for stmt in g:
    pprint.pprint(stmt)

