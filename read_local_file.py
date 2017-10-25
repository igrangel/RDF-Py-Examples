from rdflib import Graph
import pprint

g = Graph()
g.parse("sto.ttl", format="turtle")

query = """
    PREFIX sto: <https://w3id.org/i40/sto#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?sub ?pred ?obj WHERE {
         ?sub rdf:type sto:Standard
    }
    """

#print query

for row in g.query(query):
    print "Predicate:%s Object:%s"%(row[0],row[1])
