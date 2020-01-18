from util import github
import time

github.pull_repo()

while True:
    if github.pull_repo():
        print("New commit found. Repository updated.")
    time.sleep(300)