from rdflib import Graph, RDFS, Literal, BNode, URIRef
from rdflib.namespace import XSD
from SPARQLWrapper import SPARQLWrapper, JSON
import requests

# --- CONSTANTS --- #
# types of data that can be met while parsing results from DBpedia
obj_types = ['uri', 'literal', 'typed-literal', 'bnode']
# URLs of predicates to exclude from final .ttl file
excl_pred = [
  'http://dbpedia.org/ontology/thumbnail', 
  'http://dbpedia.org/ontology/wikiPageID',
  'http://dbpedia.org/ontology/wikiPageRevisionID',
  'http://dbpedia.org/ontology/wikiPageExternalLink',
  'http://purl.org/voc/vrank#hasRank',
  'http://xmlns.com/foaf/0.1/depiction',
  'http://xmlns.com/foaf/0.1/isPrimaryTopicOf'
]
# prefixes for some of URLs
prefixes = [
  { 'prefix': 'dbont', 'url': 'http://dbpedia.org/ontology/' },
  { 'prefix': 'dbprop', 'url': 'http://dbpedia.org/property/' },
  { 'prefix': 'nsprov', 'url': 'http://www.w3.org/ns/prov#' },
  { 'prefix': 'vocvr', 'url': 'http://purl.org/voc/vrank#' },
  { 'prefix': 'lingg', 'url': 'http://purl.org/linguistics/gold/' }
]

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

  # parsing returned JSON object and extracting all possible labels
  for result in results['results']['bindings']:
    if result['pred']['value'] not in excl_pred:
      res_pred = URIRef(result['pred']['value'])
      res_obj_val = result['obj']['value']
      res_obj_type = result['obj']['type']
      # types: uri, literal, typed-literal, bnode
      if res_obj_type == 'uri':
        if result['pred']['value'] == 'http://www.w3.org/ns/prov#wasDerivedFrom' and '?oldid' in res_obj_val:
          new_url = res_obj_val[:res_obj_val.find('?oldid')]
          request = requests.get(new_url)
          # status codes: 1xx - informational, 2xx - success, 3xx - redirection, 4xx - client error, 5xx - server error
          if request.status_code == 200:
            res_obj_val = new_url
          else:
            print('---' + new_url + ' DOES NOT RESPOND---')
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
        print('---UNKNOWN OBJECT TYPE FOR ' + row[1] + '---')

# adding understandable prefixes for some of URLs
for el in prefixes:
  g.bind(el['prefix'], el['url'])

# exporting updated graph to a new .ttl file
g.serialize(destination='sto-updated.ttl', format='turtle')
