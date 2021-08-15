# This file implements the service shell. You don't necessarily need to modify it for various
# algorithms. It starts gunicorn with the correct configurations and then simply waits until
# gunicorn exits.
#
# The flask server is specified to be the app object in run.py
#
# We set the following parameters:
#
# Parameter                Environment Variable              Default Value
# ---------                --------------------              -------------
# number of workers        MODEL_SERVER_WORKERS              the number of CPU cores
# timeout                  MODEL_SERVER_TIMEOUT              60 seconds

from __future__ import print_function
import multiprocessing
import os
import signal
import subprocess
import sys
from config import Config

BIND_URL = "127.0.0.1"
BIND_PORT = Config.SERVER_PORT


cpu_count = multiprocessing.cpu_count()

model_server_timeout = os.environ.get('MODEL_SERVER_TIMEOUT', 60)
model_server_workers = int(os.environ.get('MODEL_SERVER_WORKERS', 1))

def sigterm_handler( gunicorn_pid):
    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    sys.exit(0)

def start_server():
    print('Starting the server with {} workers.'.format(model_server_workers))

    gunicorn = subprocess.Popen(['gunicorn',
                                 '--timeout', str(model_server_timeout),
                                 '-k', 'gevent',
                                 '-b', '{}:{}'.format(BIND_URL,BIND_PORT),
                                 '-w', str(model_server_workers),
                                 'run:app'])

    signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler( gunicorn.pid))

    # If either subprocess exits, so do we.
    pids = set([ gunicorn.pid])
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(gunicorn.pid)
    print('Inference server exiting')

# The main routine just invokes the start function.

if __name__ == '__main__':
    start_server()
