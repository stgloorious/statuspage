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

def get_status(query_types, domains, logfile):
    status = { query : [] for query in query_types }
    processes = { domain : [] for domain in domains }

    # Start all queries in parallel
    for domain in domains:
        ping = subprocess.Popen(['ping', '-W', '1', '-c', '1', domain],
                                 stdout=logfile, stderr=logfile)
        http = subprocess.Popen(['curl', '--max-time', '2', '-f',
                                 'https://' + domain],
                                 stdout=logfile, stderr=logfile)
        dns = subprocess.Popen(['nslookup', domain],
                                 stdout=logfile, stderr=logfile)

        processes[domain] = {'ping' : ping, 'http' : http, 'dns' : dns }

    # Wait for all queries to finish
    for domain in domains:
        for query in query_types:
            processes[domain][query].wait();

    for domain in domains:
        for query_type in query_types:
            if (processes[domain][query_type].returncode):
                text='UNREACHABLE'
                color='bad'
            else:
                text='OK'
                color='good'
            status[query_type].append({ 'name'   : domain,
                                        'status' : text,
                                        'color'  : color })
    return [status[query] for query in query_types]

def get_domains(filename):
    with open(filename) as f:
        config = json.load(f)
        return config['domains']

def get_hostname(filename):
    with open(filename) as f:
        config = json.load(f)
        return config['hostname']

@app.route("/")
def index ():
    time_now = datetime.now().isoformat()
    start = time.time_ns()

    # TODO: read from config as well
    query_types = ['ping', 'http', 'dns']

    domains = get_domains('config.json')
    hostname = get_hostname('config.json')

    # For debugging only
    # with open('queries.log', 'w') as log:

    # Disable logging
    log = DEVNULL
    ping_status, http_status, dns_status = get_status(query_types,
                                                      domains,
                                                      log)

    end = time.time_ns()
    elapsed = (end - start) / 1e6
    return render_template('index.html',
                           ping_status=ping_status,
                           http_status=http_status,
                           dns_status=dns_status,
                           hostname=hostname,
                           time_now=time_now,
                           elapsed=elapsed)
