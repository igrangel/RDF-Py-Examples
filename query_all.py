from rdflib import Graph, RDFS, Literal, BNode, URIRef
from rdflib.namespace import XSD
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import json
import io

# solving decoding / encoding issues
def byteify(input):
  if isinstance(input, dict):
    return {byteify(key): byteify(value)
            for key, value in input.iteritems()}
  elif isinstance(input, list):
    return [byteify(element) for element in input]
  elif isinstance(input, unicode):
    return input.encode('utf-8')
  else:
    return input
    
# initializing an RDF graph based on STO ontology
g = Graph()
g.parse('sto.ttl', format='turtle')

# querying all standards with labels only in english
sto_query = """
  PREFIX sto: <https://w3id.org/i40/sto#>
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  SELECT ?sub ?dbPediaResource ?subType WHERE {
    ?sub rdf:type ?subType .
    ?sub sto:hasDBpediaResource ?dbPediaResource .
  }
"""

obj_types = ['uri', 'literal', 'typed-literal', 'bnode']
update_num = 0
for row in g.query(sto_query):
  # extracting the name of the standard
  resource = row[1].split('/')[4]
  sparql = SPARQLWrapper('http://dbpedia.org/sparql')
  
  # querying all triples for the resource subject
  # full link used for ?sub because names with colons cannot be put after prefix
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
    PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?pred ?obj WHERE { """ + \
          '<http://dbpedia.org/resource/' + resource + '>' """ ?pred ?obj
        } 
    """
  
  # sending query to the API
  sparql.setQuery(dbpedia_query)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  results = byteify(results)

  # parsing returned JSON object and extracting all possible labels
  for result in results['results']['bindings']:
    res_pred = URIRef(result['pred']['value'])
    res_obj_val = result['obj']['value']
    res_obj_type = result['obj']['type']

    # Types: uri / literal / typed-literal / bnode
    if res_obj_type == 'uri':
      g.add([row[0], res_pred, URIRef(res_obj_val)])
    elif res_obj_type == 'literal':
      if 'xml:lang' in result['obj']:
        g.add([row[0], res_pred, Literal(res_obj_val, result['obj']['xml:lang'])])
      else:
        g.add([row[0], res_pred, Literal(res_obj_val)])
    elif res_obj_type == 'typed-literal':
      if 'xml:lang' in result['obj']:
        g.add([row[0], res_pred, Literal(res_obj_val, result['obj']['xml:lang'], datatype=result['obj']['datatype'])])
      else:
        g.add([row[0], res_pred, Literal(res_obj_val, datatype=result['obj']['datatype'])])
    elif res_obj_type == 'bnode':
      g.add([row[0], res_pred, BNode(res_obj_val)])
    else:
      print '---UNKNOWN OBJECT TYPE FOR ' + row[1] + '---'

# exporting updated graph to a new .ttl file
g.serialize(destination='sto-updated.ttl', format='turtle')
