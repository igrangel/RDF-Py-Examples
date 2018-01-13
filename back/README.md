# Environment Installation

Enable [Anaconda 3](https://www.continuum.io/downloads).

```
$ conda env create -f dev_environment.yml
$ source activate SampleServer
```
Change the hostname and port in backend/config.py if neccessary. By default, `hostname = localhost`, `port = 5555`.

To start the server, run:

```
$ python run.py
```