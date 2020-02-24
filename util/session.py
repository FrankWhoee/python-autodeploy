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


def get(property, create_new_if_empty=0, new_value=-1):
    if property in Session:
        return Session[property]
    elif create_new_if_empty == 0:
        return -1
    elif create_new_if_empty == 1:
        set(property,new_value)
    else:
        raise ValueError("create_new_if_empty can only be 1 or 0. If 1 is used, a new property will be created, if 0 is used, no new property is created. Default value is 0.")

def write():
    f = open("session.json", "w")
    f.write(json.dumps(Session))
    f.close()

def set(property, value):
    Session[property] = value
    write()