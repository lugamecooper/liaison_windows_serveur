from os.path import join,split
from time import sleep
from os import startfile
def restart() -> None:
    sleep(10)
    test = f"{join(split(__file__)[0],'main.py')}"
    startfile("python",arguments=test)