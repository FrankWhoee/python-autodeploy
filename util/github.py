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

def has_new_update():
    response = requests.get('https://api.github.com/repos/'+repo_name+'/commits')
    data = json.loads(response.text)[0]
    return data["sha"] != sha, data["sha"]


def pull_repo() -> bool:
    is_new, sha = has_new_update()
    if is_new:
        origin.pull()
        session.set("sha", sha)
    return is_new
