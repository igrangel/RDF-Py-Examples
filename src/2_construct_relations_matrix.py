"""Module for enlarging existing ontology based on knowledge from DBpedia.
"""

from STOLandscape import Ontology, DBpedia
import numpy as np

def main():
    """Main function.
    Describes abstract algorithm of the matrix consctructing.
    """

    sto = Ontology('ttl/sto_all.ttl', 'STO')
    sto_query = """
        SELECT ?sub ?pred ?obj WHERE {
          ?sub ?pred ?obj .
        }
    """

    mtx, sub_list, prop_list = construct_mtx(sto.query(sto_query))
    #mtx_to_csv(mtx, sub_list, prop_list)
    sub_list, prop_list = prefix_assign(sub_list, prop_list)
    mtx, sub_list, prop_list = mtx_cleaner(mtx, sub_list, prop_list, False)
    subclasses(mtx, prop_list)
    #mtx_to_csv(mtx, sub_list, prop_list)
    #mtx_to_dep(mtx, sub_list, prop_list)


def construct_mtx(query_result):
    print('--> constructing matrix...')
    sub_list = []
    prop_list = []
    mtx = np.asarray([], dtype=int)
    for row in query_result:
        sub = str(row[0]).encode('utf-8', 'replace')
        pred = str(row[1])
        obj = str(row[2])
        prop = (pred + ' -> ' + obj).encode('utf-8', 'replace')
        mtx = mtx_enrich(mtx, sub_list, prop_list, sub, prop)
    return mtx, sub_list, prop_list


def mtx_enrich(mtx, sub_list, prop_list, sub, prop):
    if len(mtx) == 0:
        sub_list.append(sub)
        prop_list.append(prop)
        mtx = np.asarray([[True]], dtype=bool)
    else:
        if sub not in sub_list:
            sub_list.append(sub)
            mtx = np.vstack([mtx, np.zeros(mtx.shape[1])])
            ind = len(sub_list) - 1
        else:
            ind = sub_list.index(sub)

        if prop not in prop_list:
            prop_list.append(prop)
            mtx_tmp = mtx
            mtx = np.zeros((mtx.shape[0], mtx.shape[1]+1))
            mtx[:, :-1] = mtx_tmp
            jnd = len(prop_list) - 1
        else:
            jnd = prop_list.index(prop)

        mtx[ind, jnd] = True
    return mtx


def mtx_to_csv(mtx, sub_list, prop_list):
    print('--> saving as csv...')
    csv_mtx = np.empty((mtx.shape[0] + 1, mtx.shape[1] + 1), dtype=object)
    csv_mtx[:, 0] = np.insert(np.asarray(sub_list), 0, ''.encode('utf-8', 'replace')) #.astype(str)
    csv_mtx[0, :] = np.insert(np.asarray(prop_list), 0, ''.encode('utf-8', 'replace')) #.astype(str)
    csv_mtx[1:, 1:] = mtx.astype(int)
    np.savetxt("foo.csv", csv_mtx, delimiter=";", fmt="%s")


def sum_rows(x):
    return sum(x)


def mtx_cleaner(mtx, sub_list, prop_list, is_sum):
    print('--> cleaning matrix...')
    sub_num = mtx.shape[0]
    #prop_num = 20
    thld = 4

    mtx_sums = np.apply_along_axis(sum_rows, axis=0, arr=mtx)
    sort_args = mtx_sums.argsort()
    new_mtx_sums = mtx_sums[sort_args]
    new_prop_list = np.asarray(prop_list)[sort_args]
    is_thld = False
    while not is_thld:
        thld_args = np.where(new_mtx_sums == thld)
        thld = thld + 1
        is_thld = len(thld_args[0])
    last_arg = thld_args[0][len(thld_args[0])-1] + 1
    new_mtx = mtx[0:sub_num, sort_args]
    new_sub_list = np.asarray(sub_list)[0:sub_num]
    if is_sum:
        new_mtx = np.vstack([new_mtx, np.zeros(mtx.shape[1])])
        new_mtx[new_mtx.shape[0] - 1][:] = new_mtx_sums
        new_sub_list = np.append(new_sub_list, 'SUM')
    sort_new_mtx = new_mtx[:, last_arg:]
    return sort_new_mtx, new_sub_list, new_prop_list[last_arg:]


def prefix_assign(sub_list, prop_list):
    print('--> assigning prefixes...')
    prfxs_map = np.asarray(prefix_mapping())
    for prfx_map in prfxs_map:
        prfx = (prfx_map[0] + ':').encode('utf-8')
        url = prfx_map[1].encode('utf-8')
        for sub_cnt, sub in enumerate(sub_list):
            if url in sub:
                sub_list[sub_cnt] = sub_list[sub_cnt].replace(url, prfx)
        for prop_cnt, prop in enumerate(prop_list):
            if url in prop:
                prop_list[prop_cnt] = prop_list[prop_cnt].replace(url, prfx)
    return sub_list, prop_list


def prefix_mapping():
    return [
        ['cc', 'http://creativecommons.org/ns#'],
        ['dbo', 'http://dbpedia.org/ontology#'],
        ['dbo', 'http://dbpedia.org/ontology/'],
        ['dbr', 'http://dbpedia.org/resource#'],
        ['dbr', 'http://dbpedia.org/resource/'],
        ['deo', 'http://purl.org/spar/deo/'],
        ['dul', 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#'],
        ['geo', 'http://www.geonames.org/ontology#'],
        ['owl', 'http://www.w3.org/2002/07/owl#'],
        ['rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'],
        ['sto', 'https://w3id.org/i40/sto#'],
        ['xml', 'http://www.w3.org/XML/1998/namespace'],
        ['xsd', 'http://www.w3.org/2001/XMLSchema#'],
        ['dc11', 'http://purl.org/dc/elements/1.1/'],
        ['doap', 'http://usefulinc.com/ns/doap#'],
        ['foaf', 'http://xmlns.com/foaf/0.1/'],
        ['muto', 'http://purl.org/muto/core#'],
        ['rami', 'https://w3id.org/i40/rami#'],
        ['rdfs', 'http://www.w3.org/2000/01/rdf-schema#'],
        ['skos', 'http://www.w3.org/2004/02/skos/core#'],
        ['vann', 'http://purl.org/vocab/vann/'],
        ['voaf', 'http://purl.org/vocommons/voaf#'],
        ['schema', 'http://schema.org/'],
        ['dcterms', 'http://purl.org/dc/terms/'],
        ['dbprop', 'http://dbpedia.org/property/'],
        ['dby', 'http://dbpedia.org/class/yago/'],
        ['nsprov', 'http://www.w3.org/ns/prov#'],
        ['lingg','http://purl.org/linguistics/gold/'],
        ['wkdr','http://wikidata.dbpedia.org/resource/'],
        ['wkde','http://www.wikidata.org/entity/']
    ]


def mtx_to_dep(mtx, sub_list, prop_list):
    names = np.append(sub_list, prop_list)
    data = np.zeros((len(names), len(names)))
    data[:len(sub_list), len(sub_list):] = mtx
    data[len(sub_list):, :len(sub_list)] = np.transpose(mtx) #np.flipud(np.rot90(mtx))
    #np.savetxt("wheel/names.txt", names.astype(str), delimiter=", ", fmt="%s")
    #np.savetxt("wheel/data.txt", data.astype(int), delimiter=", ", fmt="%s")
    text_file = open("wheel/names.txt", "w")
    names_txt = np.array2string(names.astype(str), separator=', ', max_line_width=np.inf)
    text_file.write(names_txt.replace('\'', '"'))
    text_file.close()

    text_file = open("wheel/data.txt", "w")
    #arr_txt = data.astype(int).tostring().decode('utf-8')
    arr_txt = str(data.astype(int).tolist())
    text_file.write(arr_txt) #np.array2string(data.astype(int), separator=', ')
    text_file.close()


def subclass(x):
    #has_minus_one = len(np.where(x == -1)[0])
    has_plus_one = len(np.where(x == 1)[0])
    if has_plus_one:
        return False
    else:
        return True


def subclasses(mtx, prop_list):
    subs_mtx = np.empty((mtx.shape[1], mtx.shape[1]), dtype=object)
    for cnt, column in enumerate(np.transpose(mtx)):           
        new_mtx = np.transpose(mtx) - column
        res_vec = np.apply_along_axis(subclass, axis=1, arr=new_mtx)
        res_vec[cnt] = False
        subs = np.where(res_vec == True)[0]
        subs_mtx[0][cnt] = prop_list[cnt]
        if len(subs) > 0:
            subs_mtx[1:len(subs)+1, cnt] = prop_list[subs]
        subs_mtx[len(subs)+1:, cnt] = ''
    np.savetxt("subs.csv", subs_mtx.astype(str), delimiter=";", fmt="%s")


if __name__ == "__main__":
    main()
