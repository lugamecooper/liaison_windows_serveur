import os
import subprocess
import shlex

class vvv():
    def __init__(self):
        a = subprocess.Popen("ping 127.0.0.1",stdout=subprocess.PIPE)
        stdout_value=a.communicate()[0]
        print(stdout_value)

if __name__ == "__main__":
    app1version = vvv()