"""File that contains the endpoints for the app."""
import logging
import traceback

from gevent.wsgi import WSGIServer

from flask import (Flask, Response, render_template, request,
                   send_from_directory, jsonify)
from pylogging import HandlerType, setup_logger

from .config import CONFIG

from .STOLandscape import Ontology, DBpedia

logger = logging.getLogger(__name__)
app = Flask(__name__, static_folder='../../front/src')


@app.before_first_request
def init():
    """Initialize the application with defaults."""
    logger.info("App initialized")


@app.route('/')
def root():
    """Root route."""
    logger.info("route: /")
    return app.send_static_file('index.html')
    return


@app.route('/index')
def index():
    """Index route."""
    logger.info("route: /index")
    return app.send_static_file('index.html')


@app.route('/editor')
def editor():
    """Editor route."""
    logger.info("route: /editor")
    return app.send_static_file('editor.html')


@app.route('/viewer')
def viewer():
    """Viewer route."""
    logger.info("route: /viewer")
    return app.send_static_file('viewer.html')


@app.route('/vowl')
def vowl():
    """VOWL route."""
    logger.info("route: /vowl")
    return app.send_static_file('vowl.html')


@app.route('/node_modules/<path:path>')
def send_node_modules(path):
    """Server static files from node_modules."""
    logger.info("route: node_modules/{}".format(path))
    path_prefix = '../../front/node_modules'
    return send_from_directory(path_prefix, path)


@app.route('/query', methods=['POST'])
def post_sto_query():
    """Post query and get the result."""
    logger.info("route: query")
    query = request.get_json()['quer']
    headlines = request.get_json()['head']
    ontology = request.get_json()['ont']
    req_type = request.get_json()['type']
    if ontology == 'sto':
        sto = Ontology('server/ttl/sto.ttl', 'STO')
        arr = []
        for row in sto.query(query):
            arr.append(row)
    elif ontology == 'dbp':
        arr = DBpedia().query(query)
    else:
        print('Unknown ontology')
    return jsonify({'data': arr, 'heads': headlines, 'ont': ontology, 'type': req_type})


@app.route('/update', methods=['POST'])
def post_sto_update():
    """Update STO with new triple."""
    subj = request.get_json()['subj']
    pred = request.get_json()['pred']
    obj = request.get_json()['obj']
    req_type = request.get_json()['type']
    sto = Ontology('server/ttl/sto.ttl', 'STO')
    triple = [{
        "sub": { "value": subj },
        "pred": { "value": pred },
        "obj": { "value": obj, "type": "uri" }
    }]
    sto.enrich(None, triple)
    sto.export('server/ttl/sto-some.ttl')
    return jsonify({'result': 'success', 'type': req_type})


@app.route('/<path:path>')
def send_static(path):
    """Server static files."""
    logger.info("route: {}".format(path))
    path_prefix = '../../front/src'
    return send_from_directory(path_prefix, path)


def main():
    """Main entry point of the app."""
    try:
        http_server = WSGIServer((CONFIG['host'], CONFIG['port']),
                                 app,
                                 log=logging,
                                 error_log=logging)

        http_server.serve_forever()
    except Exception as exc:
        logger.error(exc.message)
        logger.exception(traceback.format_exc())
    finally:
        # Do something here
        pass
