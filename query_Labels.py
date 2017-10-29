from rdflib import Graph, RDFS, Literal
from rdflib.namespace import XSD
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

# initializing an RDF graph based on STO ontology
g = Graph()
g.parse('sto.ttl', format='turtle')

# querying all standards with labels only in english
sto_query = """
  PREFIX sto: <https://w3id.org/i40/sto#>
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  SELECT ?sub ?dbPediaResource WHERE {
  ?sub rdf:type sto:Standard .
  ?sub sto:hasDBpediaResource ?dbPediaResource .
    ?sub rdfs:label ?label
  } GROUP BY ?sub
  HAVING (group_concat(lang(?label); separator="; ") = 'en')
"""

for row in g.query(sto_query):
  # extracting the name of the standard
  resource = row[1].split('/')[4]
  sparql = SPARQLWrapper('http://dbpedia.org/sparql')
  
  # querying all triples for the resource subject
  dbpedia_query = """
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
        SELECT ?pred ?obj WHERE { """ + \
          "r:" + resource + """ ?pred ?obj
        } 
    """
  
  # sending query to the API
  sparql.setQuery(dbpedia_query)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  
  # parsing returned JSON object and extracting all possible labels
  for result in results['results']['bindings']:
    if result['pred']['value'] == 'http://www.w3.org/2000/01/rdf-schema#label':
      label_lang = result['obj']['xml:lang']
	  # excluding Russian, Arabic and Chinese languages because of the encoding-decoding issues
      if label_lang not in ['ru', 'ar', 'zh', 'en']:
        # encoding might be needed because of different scripts
        label_str = result['obj']['value'].encode(sys.stdout.encoding, errors='replace')
        g.add([row[0], RDFS.label, Literal(label_str, label_lang)])

# exporting updated graph to a new .ttl file
g.serialize(destination='sto-updated.ttl', format='turtle')
