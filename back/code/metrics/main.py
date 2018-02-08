import numpy as np
from STOLandscape import Ontology, DBpedia

def main():
    subject = 'sto:IEC_62541'
    result = data_extract(subject)
    if result:
        data, names = wheel_data(subject, result)
        save_as_text(data, names)


def data_extract(sub):
    subject = 'sto:IEC_62541'
    sto = Ontology('ttl/sto.ttl', 'STO')
    sto_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        SELECT ?dbPediaResource WHERE {
            """ + subject + """ sto:hasDBpediaResource ?dbPediaResource .
        }
    """

    for row in sto.query(sto_query):
        if row:
            resource = str(row[0])
            dbpedia_query = 'SELECT ?pred ?obj WHERE { <' + resource + '> ?pred ?obj }'
            dbpedia_result = DBpedia().query(dbpedia_query)
            return dbpedia_result
        else:
            print('No dbpedia resource found for ' + sub)
            return {}


def wheel_data(subject, result):
    dimension = len(result) + 1 # 1 is subject itself
    data = np.zeros((dimension, dimension))
    data[0,:] = np.ones(dimension)
    data[:,0] = np.ones(dimension)
    data[0,0] = 0
    names = np.asarray([subject])
    prefixes = prefixes_list()
    for row in result:
        name = row['pred']['value']
        for prefix in prefixes:
            if prefix[1] in name:
                name = name.replace(prefix[1], prefix[0] + ':')
        
        names = np.append(names, name)
    return data, names


def save_as_text(data, names):
    text_file = open('output/names.txt', 'w')
    names_txt = np.array2string(names.astype(str), separator=', ', max_line_width=np.inf)
    text_file.write(names_txt.replace('\'', '"'))
    text_file.close()

    text_file = open('output/data.txt', 'w')
    data_txt = str(data.astype(int).tolist())
    text_file.write(data_txt)
    text_file.close()


def prefixes_list():
    return [
        ['cc', 'http://creativecommons.org/ns#'],
        ['dbo', 'http://dbpedia.org/ontology#'],
        ['dbo', 'http://dbpedia.org/ontology/'],
        ['dbp', 'http://dbpedia.org/property/'],
        ['dbr', 'http://dbpedia.org/resource#'],
        ['dbr', 'http://dbpedia.org/resource/'],
        ['dby', 'http://dbpedia.org/class/yago/'],
        ['dce', 'http://purl.org/dc/elements/1.1/'],
        ['dct', 'http://purl.org/dc/terms/'],
        ['deo', 'http://purl.org/spar/deo/'],
        ['doap', 'http://usefulinc.com/ns/doap#'],
        ['dul', 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#'],
        ['foaf', 'http://xmlns.com/foaf/0.1/'],
        ['geo', 'http://www.geonames.org/ontology#'],
        ['ling','http://purl.org/linguistics/gold/'],
        ['muto', 'http://purl.org/muto/core#'],
        ['nspr', 'http://www.w3.org/ns/prov#'],
        ['owl', 'http://www.w3.org/2002/07/owl#'],
        ['rami', 'https://w3id.org/i40/rami#'],
        ['rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'],
        ['rdfs', 'http://www.w3.org/2000/01/rdf-schema#'],
        ['sch', 'http://schema.org/'],
        ['skos', 'http://www.w3.org/2004/02/skos/core#'],
        ['sto', 'https://w3id.org/i40/sto#'],
        ['vann', 'http://purl.org/vocab/vann/'],
        ['voaf', 'http://purl.org/vocommons/voaf#'],
        ['vrank', 'http://purl.org/voc/vrank#'],
        ['wike','http://www.wikidata.org/entity/'],
        ['wikdr','http://wikidata.dbpedia.org/resource/'],
        ['xml', 'http://www.w3.org/XML/1998/namespace'],
        ['xsd', 'http://www.w3.org/2001/XMLSchema#'],
    ]


if __name__ == '__main__':
    main()
