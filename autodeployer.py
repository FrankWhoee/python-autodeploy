from util import session
from util import github
import time
import subprocess, os
import yaml
from signal import signal, SIGINT
from sys import exit
from flask import Flask
import threading
import json
import traceback

global next_check

app = Flask(__name__)


@app.route('/next')
def next_check():
    data = {
        'next_check': next_check
    }
    return json.dumps(data)


@app.route('/history')
def deployment_history():
    h = session.get("deployment_history", create_new_if_empty=1, new_value=[])
    data = {
        'deployment_history': h
    }
    return json.dumps(data)


p = None
print("Running current working directory in " + str(os.getcwd()))


def start_app():
    print("autodeploy[" + config['repo'] + "]: Starting app...")
    global p
    subprocess.Popen("exec " + "pip install -r requirements.txt", stdout=subprocess.PIPE, shell=True)
    p = subprocess.Popen("exec " + "python " + config['run'], stdout=subprocess.PIPE, shell=True)


def restart_app():
    kill_app()
    start_app()


def kill_app():
    global p
    p.kill()


class deployment(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.board = 1

    def run(self):
        print("autodeploy[" + config['repo'] + "]: Autodeploy is now on.")
        while True:
            is_new, node_id = github.pull_repo()
            if is_new:
                log("New commit found. Repository has been updated and the app is being restarted.", metadata={
                    "node_id" : node_id,
                    "event":"new_commit"
                })
                print("autodeploy[" + config['repo'] + "]: New commit found. Repository updated.")
                print("autodeploy[" + config['repo'] + "]: Restarting app...")
                restart_app()
                print("autodeploy[" + config['repo'] + "]: App is running...")
                log("App was succesfully restarted.", metadata={
                    "event":"redeploy_complete"
                })
            else:
                print("autodeploy[" + config['repo'] + "]: No update found. Skipping pull...")
                log("No new commits found. Pull has been skipped. nodeid["+node_id+"]", metadata={
                    "node_id" : node_id,
                    "event":"no_new_commit"
                })
            global next_check
            delay = int(config['period']) if 'period' in config else 600
            next_check = int(time.time()) + delay
            time.sleep(delay)


def log(message: str, metadata: dict = {}):
    history: list = session.get("deployment_history", create_new_if_empty=1, new_value=[])
    history.append({
        "time": int(time.time()),
        "log": message,
        "meta": metadata
    })
    session.set("deployment_history", history)


github.pull_repo()
config = yaml.load(open("autodeploy.conf"))
meta = yaml.load(open("python-autodeploy/meta.yaml"))
d = deployment(1, "deployment", 1)
start_app()


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

log("Starting app for the first time in this session. Autodeploy version " + meta['version'], metadata={
                    "version" : meta['version'],
                    "event":"initial_deploy"
                })
try:
    d.start()
    if __name__ == '__main__' and 'api-port' in config:
        app.run(host='0.0.0.0', port=config['api-port'])
    log("Startup succesful.", metadata={
        "version": meta['version'],
        "event": "initial_deploy_success"
    })
except Exception as E:
    log("Startup failed.", metadata={
        "error": traceback.format_exc(),
        "version": meta['version'],
        "event": "initial_deploy_fail"
    })

signal(SIGINT, handler)
