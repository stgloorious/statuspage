import time
import subprocess
import json
from subprocess import DEVNULL
from flask import Flask
from flask import render_template
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

# Not really necessary for this application, but keep it for good practice
app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=2, x_proto=2, x_host=1, x_prefix=1
)

def get_status(queries, logfile):
    # Start all queries in parallel
    processes = []
    for query in queries:
        for domain in query['domains']:
            # replace '{uri}' with actual uri
            cmd = []
            for string in query['cmd']:
                cmd.append(string.replace('{uri}', domain['uri']))
            proc = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)
            domain['process'] = proc
            processes.append(proc)

    # Wait for all queries to finish
    for process in processes:
        process.wait()

    for query in queries:
        for domain in query['domains']:
            if (domain['process'].returncode):
                domain['text'] = query['text_nonzero']
                domain['color'] = query['color_nonzero']
            else:
                domain['text'] = query['text_zero']
                domain['color'] = query['color_zero']
    return queries

def get_from_config(filename, name):
    with open(filename) as f:
        config = json.load(f)
        return config[name]

@app.route("/")
def index ():
    time_now = datetime.now().isoformat()
    start = time.time_ns()

    config = 'config.json'

    query_types = get_from_config(config, 'query_types')
    domains = get_from_config(config, 'domains')
    hostname = get_from_config(config, 'hostname')

    # find compatible domains for each query type
    for query in query_types:
        query['domains'] = []
    for domain in domains:
        for supported_query in domain['supported_queries']:
            for query in query_types:
                if supported_query == query['id']:
                    query['domains'].append({'uri' : domain['uri']})

    queries = get_status(query_types, DEVNULL)

    end = time.time_ns()
    elapsed = (end - start) / 1e6
    return render_template('index.html',
                           queries=queries,
                           hostname=hostname,
                           time_now=time_now,
                           elapsed=elapsed)
