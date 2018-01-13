"""Module for enlarging existing ontology based on knowledge from DBpedia.
"""

from STOLandscape import Ontology, DBpedia
import numpy as np

def main():
    """Main function.
    Describes abstract algorithm of the matrix consctructing.
    """

    sto = Ontology('ttl/sto.ttl', 'STO')
    sto_query = """
        SELECT ?sub ?pred ?obj WHERE {
          ?sub ?pred ?obj .
        }
    """

    mtx, sub_list, prop_list = construct_mtx(sto.query(sto_query))
    mtx_to_csv(mtx, sub_list, prop_list)


def construct_mtx(query_result):
    sub_list = []
    prop_list = []
    mtx = np.asarray([], dtype=bool)

    for row in query_result:
        sub = str(row[0]).encode('utf-8', 'replace')
        pred = str(row[1])
        obj = str(row[2])
        prop = (pred + ' -- ' + obj).encode('utf-8')
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
    csv_mtx = np.empty((mtx.shape[0] + 1, mtx.shape[1] + 1), dtype=object)
    csv_mtx[:, 0] = np.asarray([''.encode('utf-8')] + sub_list)
    csv_mtx[0, :] = np.asarray([''.encode('utf-8')] + prop_list)
    csv_mtx[1:, 1:] = mtx.astype(int)
    np.savetxt("foo.csv", csv_mtx, delimiter=";", fmt="%s")


if __name__ == "__main__":
    main()
