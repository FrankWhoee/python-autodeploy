from util import github
import time
import subprocess
import yaml
from signal import signal, SIGINT
from sys import exit

github.pull_repo()
config = yaml.load(open("autodeploy.conf"))

p = subprocess.Popen("exec " + "python " + config['run'], stdout=subprocess.PIPE, shell=True)


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)


def restart_app():
    global p
    p.kill()
    p = subprocess.Popen("exec " + "python " + config['run'], stdout=subprocess.PIPE, shell=True)


def kill_app():
    global p
    p.kill()

signal(SIGINT, handler)

while True:
    if github.pull_repo():
        print("autodeploy[ " + config['repo'] + "]: New commit found. Repository updated.")
        print("autodeploy[ " + config['repo'] + "]: Restarting app...")
        restart_app()
        print("autodeploy[ " + config['repo'] + "]: App is running...")
    time.sleep(600)
