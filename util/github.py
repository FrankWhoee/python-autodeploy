import requests
from util import session
import json
from git import Repo

# Loads previous commit SHA if it exists within Session
sha = session.get("sha")

repo = Repo(".")
assert not repo.bare

origin = repo.remote("origin")


def has_new_update():
    response = requests.get('https://api.github.com/repos/vikingsdev/dentaku/commits')
    data = json.loads(response.text)[0]
    return data["sha"] != sha, data["sha"]


def pull_repo():
    is_new,sha = has_new_update()
    if is_new:
        origin.pull()
        session.set("sha",sha)

