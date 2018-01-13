"""Module for enlarging existing ontology based on knowledge from DBpedia.
"""

from STOLandscape import Ontology, DBpedia

def main():
    """Main function.
    Describes abstract algorithm of the ontology enriching.
    """

    sto = Ontology('ttl/sto_test.ttl', 'STO')
    sto_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        SELECT ?sub ?dbPediaResource WHERE {
            ?sub rdf:type ?subType .
            ?sub sto:hasDBpediaResource ?dbPediaResource .
        }
    """

    for row in sto.query(sto_query):
        subject = row[0]
        resource = row[1].split('/')[4]

        dbpedia_query = """
            SELECT ?pred ?obj WHERE { """ + \
                '<http://dbpedia.org/resource/' + resource + '>' """ ?pred ?obj
            } 
        """
        dbpedia_result = DBpedia().query(dbpedia_query)

        sto = set_blacklist(sto)
        sto.enrich(subject, dbpedia_result)
        sto = set_prefixes(sto)
        sto.export('ttl/sto_test_all.ttl')

def set_blacklist(sto):
    """Setter of ontology black list.
    Here all predicates that should be excluded while fetching data from DPpedia are specified.
    """

    #sto.blacklist.add('http://dbpedia.org/ontology/thumbnail')
    #sto.blacklist.add('http://dbpedia.org/ontology/wikiPageID')
    #sto.blacklist.add('http://dbpedia.org/ontology/wikiPageRevisionID')
    #sto.blacklist.add('http://dbpedia.org/ontology/wikiPageExternalLink')
    #sto.blacklist.add('http://purl.org/voc/vrank#hasRank')
    #sto.blacklist.add('http://xmlns.com/foaf/0.1/depiction')
    #sto.blacklist.add('http://xmlns.com/foaf/0.1/isPrimaryTopicOf')
    #sto.blacklist.add('http://www.w3.org/2000/01/rdf-schema#comment')
    #sto.blacklist.add('http://dbpedia.org/ontology/abstract')
    return sto

def set_prefixes(sto):
    """Setter of ontology prefixes.
    Here all custom prefixes are specified.
    """

    sto.set_prefix('dbont', 'http://dbpedia.org/ontology/')
    sto.set_prefix('dbprop', 'http://dbpedia.org/property/')
    sto.set_prefix('nsprov', 'http://www.w3.org/ns/prov#')
    sto.set_prefix('vocvr', 'http://purl.org/voc/vrank#')
    sto.set_prefix('lingg', 'http://purl.org/linguistics/gold/')
    return sto

if __name__ == "__main__":
    main()
