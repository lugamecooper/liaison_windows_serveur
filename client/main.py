from socket import socket,AF_INET,SOCK_STREAM
import os
import _thread
import json
import tkinter
import pickle

class main:
    def __init__(self) -> None:
        self.config = json.load(open("config.json"))
        _thread.start_new_thread(self.connexion_distant_thread,())
        _thread.start_new_thread(self.connexion_local_thread,())

        self.test_mode = None

        self.fen = tkinter.Tk(className="client_liaison_windows_serveur")
        self.fen.geometry(f"{self.fen.winfo_screenwidth()}x{self.fen.winfo_screenheight()}")

        self.menu_bar = tkinter.Menu(self.fen)
        self.menu_connection = tkinter.Menu(self.menu_bar,tearoff=0)
        self.menu_connection.add_command(label="connexion_distance",command=self.connexion_distance)
        self.menu_connection.add_command(label="connexion_local",command=self.connexion_local)
        self.menu_bar.add_cascade(label="menu_connection",menu=self.menu_connection)
        
        self.fen.config(menu=self.menu_bar)

        self.body = tkinter.Frame(self.fen)

        self.affichage_init()

        self.body.pack()

        self.fen.mainloop()
        

    def affichage_init(self):
        self.label_init = tkinter.Label(self.body,text="séléctioner une option de connection")
        self.label_init.pack()

    def connexion_distance(self):
        self.label_init.destroy()
        self.commun("distance")
        self.test_mode = 0

    def connexion_local(self):
        self.label_init.destroy()
        self.commun("local")
        self.test_mode = 1

    def commun(self,para):
        self.body.destroy()
        self.body = tkinter.Frame(self.fen)

        self.label_init = tkinter.Label(self.body,text=f"connexion {para}")
        self.zone_commande_entre = tkinter.Frame(self.body)
        self.saisie_commande = tkinter.Entry(self.zone_commande_entre,width=120)
        self.bouton_envoi_commande = tkinter.Button(self.zone_commande_entre,text="envoi de la commande",command=self.envoi_commande)

        self.label_init.pack()
        self.saisie_commande.pack()
        self.zone_commande_entre.pack()
        self.bouton_envoi_commande.pack()

        self.body.pack()

    def connexion_local_thread(self):
        while True:
            try:
                self.connexion_server_local = socket(AF_INET, SOCK_STREAM)
                self.connexion_server_local.connect((self.config[0],self.config[1]))
                break
            except:
                pass
        while True:
            message = pickle.loads(self.connexion_server_local.recv(1024))
            if message:
                print(message)

    def connexion_distant_thread(self):
        while True:
            try:
                self.connexion_server_distant = socket(AF_INET, SOCK_STREAM)
                self.connexion_server_distant.connect((self.config[2],self.config[3]))
                break
            except:
                pass
        while True:
            message = pickle.loads(self.connexion_server_distant.recv(1024))
            if message:
                print(message)

    def envoi_commande(self):
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#01#",self.saisie_commande.get()]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#01#",self.saisie_commande.get()]))

main()
