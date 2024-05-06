from socket import socket,AF_INET,SOCK_STREAM
from os.path import join,split,isdir,isfile,getsize
from subprocess import Popen,PIPE
from json import load
import os
from _thread import start_new_thread,exit as E
import re
import pickle
class main:
    def __init__(self) -> None:
        if os.name == 'nt':
            self.path_base = re.findall(r"([\w| ]*:\\)",__file__)[0] 
        else:
            self.path_base = "/"
        self.path = {}
        self.config = load(open(join(split(__file__)[0],"config.json")))
        start_new_thread(self.co_ini_distant,())
        start_new_thread(self.co_ini_local,())
        while True:
            pass

    def commande(self,commande = list,client = socket()):
        try:
            if "#01#" == commande[0]:
                client.send(pickle.dumps(["#01#",Popen(commande[1],stdout=PIPE).communicate()[0]]))
            elif "#02#" == commande[0]:
                client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
            elif "#03#" == commande[0]:
                if isdir(join(self.path[client],commande[1])):
                    self.path[client] = join(self.path[client],commande[1])
                    client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
            elif "#04#" == commande[0]:
                if os.name == "nt":
                    if self.path[client] == re.findall(r"([\w| ]*:\\)",__file__)[0]:
                        pass
                    else:
                        test = self.path[client].split("\\")
                        self.path[client] = ""
                        tempo = []
                        for i in test:
                            if i:
                                tempo.append(i)
                        test = tempo
                        for i in range(len(test)-1):
                            self.path[client] += test[i]+"\\"
                else:
                    if not self.path[client] == "/":
                        test = self.path[client].split("/")
                        test[0] = "/"
                        self.path[client] = ""
                        for i in range(len(test)-1):
                            self.path[client] += test[i]+"/"
                    else:
                        pass
                client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
            elif commande[0] == "#05#":
                tempo = join(self.path[client],commande[1])
                if isfile(tempo):
                    client.send(pickle.dumps(["#05#",commande[1],int(getsize(tempo)*1.2)]))
                    f = open(tempo, 'rb')
                    while True:
                        l = f.read(int(getsize(tempo)*1.2))
                        while (l):
                            client.send(l)
                            l = f.read(int(getsize(tempo)*1.2   ))
                        if not l:
                            client.send(None)
                            f.close()
                            break
                else:
                    client.send(pickle.dumps(["#50#",""]))
            elif commande[0] == "#06#":
                while True:
                    test = commande
                    if test:
                        if test[0] == "#06#":
                            f = open(join(self.path[client],test[1]), 'wb')
                            while True:
                                data = client.recv(int(test[2]))
                                try:
                                    if pickle.loads(data) == ["#60#",""]:
                                        f.close()
                                        client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
                                        print("test")
                                        break
                                except Exception as er:
                                    pass
                                f.write(data)
                                data = ""
                        elif test[0] == "#60#":
                            break
                        break
                client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
            elif commande[0] == "#07#":
                if isdir(join(self.path[client],commande[1])):
                    pass
                else:
                    os.mkdir(join(self.path[client],commande[1]))
                    client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
            elif commande[0] == "#08#":
                if isdir(join(self.path[client],commande[1])):
                    if os.name == "nt":
                        os.system(f"rmdir {join(self.path[client],commande[1])} /S /Q")
                    else:
                        os.system(f"rm {join(self.path[client],commande[1])} -r")
                else:
                    os.remove(join(self.path[client],commande[1]))
                client.send(pickle.dumps(["#03#",os.listdir(self.path[client])]))
        except Exception as er:
            try:
                client.send(pickle.dumps(["#er#",f"{er}".encode("utf-8")]))
            except:
                pass

    def on_new_client_distant(self,client = socket):
        client.send(pickle.dumps(["#01#",os.name,self.config[2],self.config[3]]))
        while True:
            try:
                msg_recu = pickle.loads(client.recv(4096))
            except:
                self.path.pop(client)
                break
            if msg_recu and "#" in msg_recu[0]:
                start_new_thread(self.commande,(msg_recu,client,))

    def co_ini_distant(self):
        if self.config[2] == "127.0.0.1":
            E()
        while True:
            self.connexion_principale_distant = socket(AF_INET, SOCK_STREAM)
            try:
                self.connexion_principale_distant.bind((self.config[2],self.config[3]))
            except Exception as er:
                E()
            self.connexion_principale_distant.listen(5)
            self.client,info_connexion = self.connexion_principale_distant.accept()
            del info_connexion
            start_new_thread(self.on_new_client_distant,(self.client,))


    def on_new_client_local(self,client = socket):
        self.path[client] = self.path_base
        client.send(pickle.dumps(["#01#",os.name,self.config[0],self.config[1]]))
        while True:
            try:
                msg_recu = pickle.loads(client.recv(4096))
            except:
                self.path.pop(client)
                break
            if msg_recu and "#" in msg_recu[0]:
                self.commande(msg_recu,client)

    def co_ini_local(self):
        while True:
            self.connexion_principale_local = socket(AF_INET, SOCK_STREAM)
            try:
                self.connexion_principale_local.bind((self.config[0],self.config[1]))
            except Exception as er:
                E()
            self.connexion_principale_local.listen(5)
            self.client,info_connexion = self.connexion_principale_local.accept()
            del info_connexion
            start_new_thread(self.on_new_client_local,(self.client,))

main()