from util import github
import time
import subprocess
import yaml

github.pull_repo()
config = yaml.load(open("autodeploy.conf"))

p = subprocess.Popen("exec " + "python " + config['run'], stdout=subprocess.PIPE, shell=True)


def restart_app():
    global p
    p.kill()
    p = subprocess.Popen("exec " + "python " + config['run'], stdout=subprocess.PIPE, shell=True)


def kill_app():
    global p
    p.kill()


while True:
    try:
        try:
            if github.pull_repo():
                print("autodeploy[ " + config['repo'] + "]: New commit found. Repository updated.")
                print("autodeploy[ " + config['repo'] + "]: Restarting app...")
                restart_app()
                print("autodeploy[ " + config['repo'] + "]: App is running...")
            time.sleep(300)
        except:
            kill_app()
    except KeyboardInterrupt:
        print("Ending process...")
        kill_app()
