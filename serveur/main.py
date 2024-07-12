from socket import socket,AF_INET,SOCK_STREAM
from os.path import join,isdir,isfile,getsize,split
from subprocess import Popen,PIPE
from json import load,dump
from os import name,listdir,mkdir,system,remove,rename
from _thread import start_new_thread,exit as E
from re import findall
from pickle import loads,dumps
from restart import restart
from time import sleep

class main:
    def __init__(self) -> None:
        if not isdir(join(split(__file__)[0],"users")):
            mkdir(join(split(__file__)[0],"users"))
            dump({"admin":["admin",None,"root"]},open(join(split(__file__)[0],join("users","admin.json")),"w"))
        self.liste_classe_utilisateur = listdir(join(split(__file__)[0],"users"))
        if self.liste_classe_utilisateur == []:
            self.liste_classe_utilisateur = None
        if name == 'nt':
            self.path_base = findall(r"([\w| ]*:\\)",__file__)[0] 
        else:
            self.path_base = "/"
        self.path = {}
        self.config = load(open(join(split(__file__)[0],"config.json")))
        start_new_thread(self.co_ini_distant,())
        start_new_thread(self.co_ini_local,())
        while True:
            try:
                input()
                self.restart()
            except:
                exit()

    def restart(self):
        start_new_thread(restart,())
        sleep(9.5)
        for client in self.path:
            client.send(dumps(["#99#",""]))
        exit()

    def commande(self,commande = list,client = socket(),base_path = str()):
        try:
            if "#01#" == commande[0]:
                client.send(dumps(["#01#",Popen(commande[1],shell=True,stdout=PIPE).communicate()[0]]))
            elif "#02#" == commande[0]:
                sleep(0.5)
                client.send(dumps(["#03#",listdir(self.path[client])]))
            elif "#03#" == commande[0]:
                if isdir(join(self.path[client],commande[1])):
                    self.path[client] = join(self.path[client],commande[1])
                    client.send(dumps(["#03#",listdir(self.path[client])]))
            elif "#04#" == commande[0]:
                if name == "nt":
                    if self.path[client] == base_path:
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
                    if not self.path[client] == base_path:
                        test = self.path[client].split("/")
                        test[0] = "/"
                        self.path[client] = ""
                        for i in range(len(test)-1):
                            self.path[client] += test[i]+"/"
                    else:
                        pass
                client.send(dumps(["#03#",listdir(self.path[client])]))
            elif commande[0] == "#05#":
                tempo = join(self.path[client],commande[1])
                if isfile(tempo):
                    client.send(dumps(["#05#",commande[1],int(getsize(tempo)*1.2)]))
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
                    client.send(dumps(["#50#",""]))
            elif commande[0] == "#06#":
                while True:
                    test = commande
                    if test:
                        if test[0] == "#06#":
                            f = open(join(self.path[client],test[1]), 'wb')
                            while True:
                                data = client.recv(int(test[2]))
                                try:
                                    print(loads(data))
                                    if loads(data) == ["#60#",""]:
                                        f.close()
                                        client.send(dumps(["#03#",listdir(self.path[client])]))
                                        break
                                except Exception as er:
                                    pass
                                f.write(data)
                                data = ""
                            break
                        elif test[0] == "#60#":
                            break
                        break
                client.send(dumps(["#03#",listdir(self.path[client])]))
            elif commande[0] == "#07#":
                if isdir(join(self.path[client],commande[1])):
                    pass
                else:
                    mkdir(join(self.path[client],commande[1]))
                    client.send(dumps(["#03#",listdir(self.path[client])]))
            elif commande[0] == "#08#":
                if isdir(join(self.path[client],commande[1])):
                    if name == "nt":
                        system(f"rmdir {join(self.path[client],commande[1])} /S /Q")
                    else:
                        system(f"rm {join(self.path[client],commande[1])} -r")
                else:
                    remove(join(self.path[client],commande[1]))
                client.send(dumps(["#03#",listdir(self.path[client])]))
            elif commande[0] == "#09#":
                try:
                    rename(commande[1][0],commande[1][1])
                    client.send(dumps(["#03#",listdir(self.path[client])]))
                except:
                    client.send(dumps(["#er#","une erreure est survenue lors du renommage du fichier ou du dossier"]))
        except Exception as er:
            try:
                client.send(dumps(["#er#",f"{er}"]))
            except:
                pass

    def on_new_client_distant(self,client = socket):
        connected = False
        self.path[client] = self.path_base
        path_base = self.path_base
        client.send(dumps(["#00#",name,self.config[2],self.config[3],self.liste_classe_utilisateur]))
        while True:
            try:
                msg_recu = loads(client.recv(4096))
            except:
                self.path.pop(client)
                break
            if msg_recu and "#" in msg_recu[0] and connected:
                self.commande(msg_recu,client,path_base)
            elif msg_recu and "#81#" == msg_recu[0] and not connected:
                connected,path_base = self.connection(msg_recu,client)
                if path_base == None:
                    path_base = self.path_base
                sleep(1)
                if connected:
                    client.send(dumps(["#81#",connected]))
                    sleep(0.1)
                    client.send(dumps(["#03#",listdir(self.path[client])]))
                else:
                    client.send(dumps(["#81#",connected]))

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
        connected = False
        self.path[client] = self.path_base
        path_base = self.path_base
        client.send(dumps(["#00#",name,self.config[0],self.config[1],self.liste_classe_utilisateur]))
        while True:
            try:
                msg_recu = loads(client.recv(4096))
            except:
                self.path.pop(client)
                break
            if msg_recu and "#" in msg_recu[0] and connected:
                self.commande(msg_recu,client,path_base)
            elif msg_recu and "#81#" == msg_recu[0] and not connected:
                connected,path_base = self.connection(msg_recu,client)
                if path_base == None:
                    path_base = self.path_base
                sleep(1)
                if connected:
                    client.send(dumps(["#81#",connected]))
                    sleep(0.1)
                    client.send(dumps(["#03#",listdir(self.path[client])]))
                else:
                    client.send(dumps(["#81#",connected]))

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

    def connection(self,msg_recu,client = socket()):
        connection_valide = False
        path_base = None
        try:
            liste_login = load(open(join(split(__file__)[0],join("users",self.liste_classe_utilisateur[self.liste_classe_utilisateur.index(msg_recu[-1])]))))
            if liste_login.get(msg_recu[1]["user"])[0] == msg_recu[1]["password"]:
                connection_valide = True
                if liste_login.get(msg_recu[1]["user"])[1]:
                    self.path[client] = liste_login.get(msg_recu[1]["user"])[1]
                    path_base = liste_login.get(msg_recu[1]["user"])[1]
        except:
            pass
        return connection_valide,path_base

main()