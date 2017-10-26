from rdflib import Graph
import pprint
from SPARQLWrapper import SPARQLWrapper, JSON

g = Graph()
g.parse("sto.ttl", format="turtle")

query = """
    PREFIX sto: <https://w3id.org/i40/sto#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?sub ?dbPediaResource ?wikiDataEntity WHERE {
         ?sub rdf:type sto:Standard .
         OPTIONAL{
    		?sub sto:hasDBpediaResource ?dbPediaResource .
            ?sub sto:hasWikidataEntity ?wikiDataEntity
         }
    }
    """

# print query

# If the wikidata resource is not filled up
# check for the dbPediaResource
# If the dbPediaResource has a wikidata resource get it and insert it in a the KG
#for row in g.query(query):
#    if row[1]:
       # print ('dbPedia ' + row[1])

sparql = SPARQLWrapper("http://dbpedia-live.openlinksw.com/sparql/")
sparql.setQuery("""
     PREFIX dbo: <http://dbpedia.org/ontology/> 
     PREFIX owl: <http://www.w3.org/2002/07/owl#>
     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
     PREFIX dc: <http://purl.org/dc/elements/1.1/>
     PREFIX r: <http://dbpedia.org/resource/>
     PREFIX dbpedia2: <http://dbpedia.org/property/>
     PREFIX dbpedia: <http://dbpedia.org/>
     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

select ?pred ?obj where { 
  r:IEC_62264 ?pred ?obj
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print('predicate  ' + result["pred"]["value"] + '   object   ' + result["obj"]["value"])
