from socket import socket,AF_INET,SOCK_STREAM
from os.path import join,split
from subprocess import Popen,PIPE
from json import load
from _thread import start_new_thread,exit as E

class main:
    def __init__(self) -> None:
        self.config = load(open(join(split(__file__)[0],"config.json")))
        start_new_thread(self.on_new_client_distant,())
        start_new_thread(self.on_new_client_local,())
        while True:
            pass

    def commande(self,commande,client):
        try:
            client.send(Popen("127.0.0.1",stdout=PIPE).communicate()[0])
        except Exception as er:
            client.send(er)

    def on_new_client_distant(self,client):
        while True:
            try:
                msg_recu = client.recv(4096).decode('UTF-8')
            except:
                break
            if msg_recu:
                self.commande(msg_recu,client)

    def co_ini_distant(self):
        if self.config[2] == "127.0.0.1":
            E()
        while True:
            self.connexion_principale_distant = socket(AF_INET, SOCK_STREAM)
            try:
                self.connexion_principale_distant.bind((self.config[2],self.config[3]))
            except Exception as er:
                print(er)
                input()
                E()
            self.connexion_principale_distant.listen(5)
            self.client,info_connexion = self.connexion_principale_distant.accept()
            del info_connexion
            start_new_thread(self.on_new_client_distant,(self.client,))


    def on_new_client_local(self,client):
        while True:
            try:
                msg_recu = client.recv(4096).decode('UTF-8')
            except:
                break
            if msg_recu:
                self.commande(msg_recu,client)

    def co_ini_local(self):
        if self.config[0] == "127.0.0.1":
            E()
        while True:
            self.connexion_principale_local = socket(AF_INET, SOCK_STREAM)
            try:
                self.connexion_principale_local.bind((self.config[0],self.config[1]))
            except Exception as er:
                print(er)
                input()
                E()
            self.connexion_principale_local.listen(5)
            self.client,info_connexion = self.connexion_principale_local.accept()
            del info_connexion
            start_new_thread(self.on_new_client_local,(self.client,))