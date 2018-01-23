# Web STO
Web application for working with STO.

## Running
Make sure to have [Anaconda 3](https://www.continuum.io/downloads) and [npm](https://www.npmjs.com/get-npm).

When launching the server for the first time, run `$ bash setup-from-scratch.sh` for Unix systems and `$ setup-from-scratch.bat` for Windows.

For the second launch and later on, use `$ bash run.sh` for Unix systems and `$ run.bat` for Windows (all scriptes are located in the root folder).

By default, the app will be available on [http://localhost:5555/](http://localhost:5555/).

## Using
Main - Describes the purpose of the website and the area of interest of our research.
Editor - Provides a possibility to query knowledgebases of STO and DBpedia and to add any triple to the STO.
Viewer - Visualizes the STO using the library WebVOWL.
Wheel - Visualizes main entities of the STO using the library DependencyWheel.
Notebook (in development) - Provides a possibility to query the STO / DBpedia and keep all the extracted data in one place.