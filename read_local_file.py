from rdflib import Graph
import pprint

g = Graph()
g.parse("sto.ttl", format="turtle")

print("--- start: turtle ---")
print(g.serialize(format="turtle"))
print("--- end: turtle ---\n")

