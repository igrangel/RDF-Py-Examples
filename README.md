# Web STO
Web application for working with STO.

## Setup
Make sure to have [Anaconda 3](https://www.continuum.io/downloads) for Python 3.6 and [npm](https://www.npmjs.com/get-npm).

When launching the server for the first time, run `$ bash setup-from-scratch.sh` for Unix systems and `$ setup-from-scratch.bat` for Windows.

For the second launch and later on, use `$ bash run.sh` for Unix systems and `$ run.bat` for Windows (all scriptes are located in the root folder).

By default, the app will be available on [http://localhost:5555/](http://localhost:5555/).

## Usage
Main - Describes the purpose of the website and the area of interest of our research.
Editor - Provides a possibility to query knowledgebases of STO and DBpedia and to add any triple to the STO.
Viewer - Visualizes the STO using the library WebVOWL.
Wheel - Visualizes main entities of the STO using the library DependencyWheel.
Notebook (in development) - Provides a possibility to query the STO / DBpedia and keep all the extracted data in one place.

### How to prepare data for Wheel
1) Navigate to `back/server/sto_graph`.

2) Activate the environment created within Setup by `source activate websto` (for Unix systems) or `activate websto` (for Windows systems).

3) If you want first to fetch all the data from DBpedia through DBpedia links in the knowledgebase, proceed to the file `1_fetch_all_from_dbpedia.py`. Substitute the path in the `sto = Ontology('ttl/sto.ttl', 'STO')` with yours. Update prefixes, blacklist and path to the output file if needed and run the python file with `python 1_fetch_all_from_dbpedia.py`.

4) Open the file `2_construct_relations_matrix.py`. Again, change the path to your .ttl file here `sto = Ontology('ttl/sto_all.ttl', 'STO')`. The code in the file aims to create a dependency matrix for the ontology that depicts relations between every subject and every pair predicate->object, where 1 denotes that there is such a triple and 0 otherwise. The matrix is sorted by the number of triples for each predicate->object pair in ascending order.

The code generates 2 .csv files (full dependency matrix, list of subclasses of precate->object pairs) and 2 .txt files (for Wheel).

In the function `mtx_cleaner(...)` you can control the number of subjects `sub_num` and the number of predicate->object pairs `thld` in the files that will be base for a wheel. `sub_num` is just an absolute value of subjects and `thld` is a threshold for the number of triples that predicate->object pair is part of in the sordet matrix. That is used to ensure that only most common pairs will appear on the chart.

5) Execute `python 2_construct_relations_matrix.py`. Resulting files can be found in the folders `wheel/` and `csv/`. For updating the wheel chart, feel free to copy files `wheel/data.txt` and `wheel/names.txt` to the `../../../front/src/data`.