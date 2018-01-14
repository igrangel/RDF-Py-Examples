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
    mtx, sub_list, prop_list = mtx_cleaner(mtx, sub_list, prop_list)
    mtx_to_csv(mtx, sub_list, prop_list)


def construct_mtx(query_result):
    sub_list = []
    prop_list = []
    mtx = np.asarray([], dtype=int)

    for row in query_result:
        sub = str(row[0]).encode('utf-8', 'replace')
        pred = str(row[1])
        obj = str(row[2])
        prop = (pred + ' -- ' + obj).encode('utf-8', 'replace')
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
    csv_mtx[:, 0] = np.insert(np.asarray(sub_list), 0, ''.encode('utf-8', 'replace'))
    csv_mtx[0, :] = np.insert(np.asarray(prop_list), 0, ''.encode('utf-8', 'replace'))
    csv_mtx[1:, 1:] = mtx.astype(int)
    np.savetxt("foo.csv", csv_mtx, delimiter=";", fmt="%s")


def sum_rows(x):
    return sum(x)


def mtx_cleaner(mtx, sub_list, prop_list):
    mtx_sums = np.apply_along_axis(sum_rows, axis=0, arr=mtx)
    sort_args = mtx_sums.argsort()
    new_mtx_sums = mtx_sums[sort_args]
    new_prop_list = np.asarray(prop_list)[sort_args]
    one_args = np.where(new_mtx_sums == 1)
    last_one_arg = one_args[0][len(one_args[0])-1] + 1
    mtx = np.vstack([mtx, np.zeros(mtx.shape[1])])
    new_mtx = mtx[:, sort_args]
    new_mtx[mtx.shape[0] - 1][:] = new_mtx_sums
    sort_new_mtx = new_mtx[:, last_one_arg:]
    sub_list.append('SUM')
    return sort_new_mtx, sub_list, new_prop_list[last_one_arg:]


if __name__ == "__main__":
    main()
