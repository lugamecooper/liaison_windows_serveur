import socket
import os
import _thread
import json
import tkinter

class main:
    def __init__(self) -> None:
        self.test_creation = 0

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
        self.test_creation = 1

    def connexion_local(self):
        self.label_init.destroy()
        self.commun("local")
        self.test_creation = 1

    def commun(self,para):
        self.body.destroy()
        self.body = tkinter.Frame(self.fen)

        self.label_init = tkinter.Label(self.body,text=f"connexion {para}")
        self.zone_commande_entre = tkinter.Frame(self.body)
        self.saisie_commande = tkinter.Entry(self.zone_commande_entre,width=120)

        self.label_init.pack()
        self.saisie_commande.pack()
        self.zone_commande_entre.pack()

        self.body.pack()

    def connexion_local_thread(self):
        pass

    def connexion_distant_thread(self):
        pass

main()
