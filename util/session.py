import json
import os

Session = {}

if os.path.exists("session.json"):
    print("Found session file.")
    with open('session.json') as json_file:
        Session = json.load(json_file)
else:
    print("Session file not found. Creating new one at " + os.path.abspath("session.json"))
    f = open("session.json", "w")
    f.write("{}")
    f.close()


def get(property):
    if property in Session:
        return Session[property]
    else:
        Session[property] = -1
        write()
        return -1

def write():
    f = open("session.json", "w")
    f.write(json.dumps(Session))
    f.close()

def set(property, value):
    Session[property] = value
    write()