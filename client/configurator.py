from json import load,dump
from os.path import join,split
from socket import gethostbyname,gethostname
config = load(open(join(split(__file__)[0],"config.json")))
if len(config) == 4:
    config = [config[0],config[1],config[2],config[3]]
else:
    config = []
    config.append(gethostbyname(gethostname()))
    config.append(5000)
    config.append("127.0.0.1")
    config.append(5001)
print(f"config locale {config[0]}\n{config[1]}")
test_1 = int(input("voullez vous la modifiez ? [1]oui [0]non "))
print("\n")
if test_1:
    config[0] = input("adresse ip ? ")
    config[1] = int(input("port réseaux ?"))
    print("\n\n")

print(f"config distante {config[2]}\n{config[3]}")
test_2 = int(input("voullez vous la modifiez ? [1]oui [0]non "))
print("\n")
if test_2:
    config[2] = input("adresse ip ? ")
    config[3] = int(input("port réseaux ?"))
    print("\n\n")

dump(config,open(join(split(__file__)[0],"config.json"),"w"))