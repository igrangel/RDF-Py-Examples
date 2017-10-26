from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

g = Graph()
g.parse("sto.ttl", format="turtle")

query = """
    PREFIX sto: <https://w3id.org/i40/sto#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?sub ?dbPediaResource WHERE {
         ?sub rdf:type sto:Standard .
         ?sub sto:hasDBpediaResource ?dbPediaResource .
    } LIMIT 1    
    """

    # check for the dbPediaResource
    # If the dbPediaResource has a wikidata resource get it and insert it in a the KG
for row in g.query(query):
    resource = row[1].split('/')[4]

    sparql = SPARQLWrapper("http://dbpedia-live.openlinksw.com/sparql/")
    prefixes = """
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
    """
    second_query = """
        select ?pred ?obj where {
      """ + "r:" + resource + """ ?pred ?obj
    } 
    """
    #print prefixes + second_query;

    sparql.setQuery(prefixes + second_query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print('predicate  ' + result["pred"]["value"] + '   object   ' + result["obj"]["value"])
        # print result

