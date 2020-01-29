import json

import requests
import yaml
from git import Repo
from util import session

# Loads previous commit node_id if it exists within Session
node_id = session.get("node_id")

repo = Repo("")
assert not repo.bare

origin = repo.remote("origin")
api_url = origin.refs
config = yaml.load(open("autodeploy.conf"))
repo_name = config['repo']


def remaining_rate() -> int:
    response = requests.get('https://api.github.com/rate_limit')
    data = json.loads(response.text)
    return data["rate"]["remaining"]


def has_new_update():
    if remaining_rate() > 3:
        url = 'https://api.github.com/repos/' + repo_name + '/commits' + ('?sha=' + str(config['branch']) if 'branch' in config else '')
        response = requests.get(url)
        data = json.loads(response.text)[0]
        result = data["node_id"] != node_id, data["node_id"]
        print("autodeploy[ " + config['repo'] + "]: Current node_id: " + node_id)
        if not result:
            print("autodeploy[" + config['repo'] + "]: Printing response from GitHub:")
            print(data)
        return result
    else:
        return False, "-1"


def pull_repo() -> bool:
    global node_id
    is_new, node_id = has_new_update()
    if is_new:
        origin.pull()
        session.set("node_id", node_id)
    return is_new
