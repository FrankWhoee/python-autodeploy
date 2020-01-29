import json

import requests
import yaml
from git import Repo
from util import session

# Loads previous commit SHA if it exists within Session
sha = session.get("sha")

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
        url = 'https://api.github.com/repos/' + repo_name + '/commits' + ('?branch=' + config['branch'] if 'branch' in config else '')
        response = requests.get(url)
        data = json.loads(response.text)[0]
        result = data["sha"] != sha, data["sha"]
        print("autodeploy[ " + config['repo'] + "]: Current SHA: " + sha)
        if not result:
            print("autodeploy[ " + config['repo'] + "]: Printing response from GitHub:")
            print(data)
        return result
    else:
        return False, "-1"


def pull_repo() -> bool:
    global sha
    is_new, sha = has_new_update()
    if is_new:
        origin.pull()
        session.set("sha", sha)
    return is_new
