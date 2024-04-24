from socket import socket,AF_INET,SOCK_STREAM
import os
import _thread
import json
import tkinter
import pickle
from time import sleep
import tkinter.filedialog

class main:
    def __init__(self) -> None:
        self.config = json.load(open("config.json"))
        _thread.start_new_thread(self.connexion_distant_thread,())
        _thread.start_new_thread(self.connexion_local_thread,())

        self.test_mode = None
        self.message_local = None
        self.message_distant = None
        self.path_down = None
        self.path_fichier_envoi = None

        self.fen = tkinter.Tk(className="client_liaison_windows_serveur")
        self.fen.geometry(f"{self.fen.winfo_screenwidth()}x{self.fen.winfo_screenheight()}")
        self.fen.state("zoomed")

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
        self.test_mode = 0
        self.commun("distance")
        
    def connexion_local(self):
        self.label_init.destroy()
        self.test_mode = 1
        self.commun("local")
        
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

        self.div_explorateur = tkinter.Frame(self.fen)
        self.listbox = tkinter.Listbox(self.div_explorateur)
        scrollbar = tkinter.Scrollbar(self.div_explorateur)

        self.listbox.config(yscrollcommand=scrollbar.set,height=25,width=125)
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#02#"]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#02#"]))
        message = None


        self.frame_exploreur = tkinter.Frame(self.div_explorateur)
        self.bouton_déplacement_dossier = tkinter.Button(self.frame_exploreur,text="ouvrir le dossier",command=self.avance_fichier)
        self.bouton_retour_dossier = tkinter.Button(self.frame_exploreur,text="retour en arrière",command=self.recul_fichier)
        
        self.div_bouton = tkinter.Frame(self.div_explorateur)
        
        self.select_folder = tkinter.Button(self.div_bouton,text="choisissez un dossier pour le téléchargement",command=self.selectionner_recup_fichier)
        self.bouton_down_fichier = tkinter.Button(self.div_bouton,text="télécharger le fichier",command=self.test_mode)
        self.select_file = tkinter.Button(self.div_bouton,text="choisissez un fichier pour l'envoi",command=self.selectionner_envoi_fichier)
        self.bouton_up_fichier = tkinter.Button(self.div_bouton,text="envoie du fichier",command=self.test_mode)

        sleep(1)
        while True:
            if not self.test_mode:
                if self.message_distant:
                    message = self.message_distant
            else:
                if self.message_local:
                    message = self.message_local
            if message:
                break
        for i in message:
            self.listbox.insert(tkinter.END,i)
        scrollbar.config(command=self.listbox.yview)
        
        self.div_explorateur.pack()
        
        self.bouton_déplacement_dossier.pack(side=tkinter.LEFT,anchor="n")
        self.bouton_retour_dossier.pack(side=tkinter.LEFT,anchor="n")
        self.frame_exploreur.pack(side="top",anchor="n")
        self.div_bouton.pack(side="bottom")

        self.bouton_down_fichier.pack(side=tkinter.RIGHT,anchor="se")
        self.select_folder.pack(side=tkinter.RIGHT,anchor="se")

        self.bouton_up_fichier.pack(side=tkinter.LEFT,anchor="sw")
        self.select_file.pack(side=tkinter.LEFT,anchor="sw")

        self.listbox.pack(side=tkinter.LEFT)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        

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
            try:
                self.message_local = pickle.loads(self.connexion_server_local.recv(1024))
            except:
                self.message_local = None
                pass
            if self.message_local:
                print(self.message_local)
                sleep(1)
                if self.message_local[0] == "#03#":
                    self.listbox.delete(0,tkinter.END)
                    for i in self.message_local[1]:
                        self.listbox.insert(tkinter.END,i)
                    self.listbox.update()

    def connexion_distant_thread(self):
        while True:
            try:
                self.connexion_server_distant = socket(AF_INET, SOCK_STREAM)
                self.connexion_server_distant.connect((self.config[2],self.config[3]))
                break
            except:
                pass
        while True:
            try:
                self.message_distant = pickle.loads(self.connexion_server_distant.recv(1024))
            except:
                self.message_distant = None
                pass
            if self.message_distant:
                print(self.message_distant)
                sleep(1)
                if self.message_distant[0] == "#03#":
                    self.listbox.delete(0,tkinter.END)
                    for i in self.message_distant[1]:
                        self.listbox.insert(tkinter.END,i)
                    self.listbox.update()

    def envoi_commande(self):
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#01#",self.saisie_commande.get()]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#01#",self.saisie_commande.get()]))

    def avance_fichier(self):
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#03#",self.listbox.get(self.listbox.curselection())]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#03#",self.listbox.get(self.listbox.curselection())]))

    def recul_fichier(self):
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#04#"]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#04#",]))

    def selectionner_recup_fichier(self):
        test = tkinter.filedialog.askdirectory(title="séléctionner le dossier pour le téléchargement", initialdir=self.path_down)
        if test:
            self.path_down = test
            self.select_folder.config(text=f"changer de dossier pour le téléchargement\ndossier actuelle : '{self.path_down}'")
            self.select_folder.update()

    def selectionner_envoi_fichier(self):
        test = tkinter.filedialog.askopenfile(title="séléctionner le fichier à envoyer")
        self.file_sendable = test
        if test:
            self.path_fichier_envoi = test.name
            self.select_file.config(text=f"changer de fichier pour le téléchargement\nfichier actuelle : '{self.path_fichier_envoi}'")
            self.select_file.update()
main()
