from os.path import join,split
from time import sleep
from os import startfile
class restart:
    def test() -> None:
        sleep(10)
        startfile(f"python",arguments=f"{join(split(__file__)[0],"main.py")}")
restart()