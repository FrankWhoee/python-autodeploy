from util import session
from util import github
import time
import subprocess, os
import yaml
from signal import signal, SIGINT
from sys import exit

p = None
print("Running current working directory in " + str(os.getcwd()))

def start_app():
    global p
    p = subprocess.Popen("exec " + "pip install -r requirements.txt", stdout=subprocess.PIPE, shell=True)
    p = subprocess.Popen("exec " + "python " + config['run'], stdout=subprocess.PIPE, shell=True)

def restart_app():
    kill_app()
    start_app()


def kill_app():
    global p
    p.kill()


github.pull_repo()
config = yaml.load(open("autodeploy.conf"))
start_app()


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


signal(SIGINT, handler)

while True:
    if github.pull_repo():
        print("autodeploy[ " + config['repo'] + "]: New commit found. Repository updated.")
        print("autodeploy[ " + config['repo'] + "]: Restarting app...")
        restart_app()
        print("autodeploy[ " + config['repo'] + "]: App is running...")
    time.sleep(int(config['period']) if 'period' in config else 600)
