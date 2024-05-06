from socket import socket,AF_INET,SOCK_STREAM
import os
import _thread
import json
import tkinter
import pickle
from time import sleep
import tkinter.filedialog
from os.path import join,getsize,isfile

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
        self.file_size = None

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
        self.bouton_actualisation = tkinter.Button(self.frame_exploreur,text="actualiser",command=self.actualiser_fonction)
        self.bouton_nouveau_dossier = tkinter.Button(self.frame_exploreur,text="nouveau dossier",command=self.nouveau_dossier)
        self.bouton_suprimer_dossier = tkinter.Button(self.frame_exploreur,text="suprimer l'élément séléctioner",command=self.suprimer_dossier_fonction)


        self.div_bouton = tkinter.Frame(self.div_explorateur)
        
        self.select_folder = tkinter.Button(self.div_bouton,text="choisissez un dossier pour le téléchargement",command=self.selectionner_recup_fichier)
        self.bouton_down_fichier = tkinter.Button(self.div_bouton,text="télécharger le fichier",command=self.down_file)
        self.select_file = tkinter.Button(self.div_bouton,text="choisissez un fichier pour l'envoi",command=self.selectionner_envoi_fichier)
        self.bouton_up_fichier = tkinter.Button(self.div_bouton,text="envoie du fichier",command=self.up_file)

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
        self.bouton_actualisation.pack(side=tkinter.LEFT,anchor="n")
        self.bouton_déplacement_dossier.pack(side=tkinter.LEFT,anchor="n")
        self.bouton_retour_dossier.pack(side=tkinter.LEFT,anchor="n")
        self.bouton_nouveau_dossier.pack(side=tkinter.RIGHT,anchor="n")
        self.bouton_suprimer_dossier.pack(side=tkinter.RIGHT,anchor="n")
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
        if test:
            self.file_sendable = test
            self.file_size = getsize(test.name)
            self.path_fichier_envoi = test.name
            self.select_file.config(text=f"changer de fichier pour l'envoi\nfichier actuelle : '{self.path_fichier_envoi}'")
            self.select_file.update()

    def down_file(self):
        if self.test_mode:
            client = self.connexion_server_local
            if self.path_down:
                if self.listbox.get(self.listbox.curselection()):
                    client.send(pickle.dumps(["#05#",self.listbox.get(self.listbox.curselection())]))
                    while True:
                        test = self.message_local
                        if test:
                            if test[0] == "#05#":
                                with open(join(self.path_down,test[1]), 'wb') as f:
                                        data = client.recv(int(test[2]))
                                        try:
                                            if data.decode("utf-8") == "stop":
                                                f.close()
                                                break
                                        except:
                                            pass 
                                        f.write(data)
                                break
                            elif test[0] == "#50#":
                                break
        if not self.test_mode:
            client = self.connexion_server_distant
            if self.path_down:
                if self.listbox.get(self.listbox.curselection()):
                    client.send(pickle.dumps(["#05#",self.listbox.get(self.listbox.curselection())]))
                    while True:
                        test = self.message_local
                        if test:
                            if test[0] == "#05#":
                                with open(join(self.path_down,test[1]), 'wb') as f:
                                        data = client.recv(int(test[2]))
                                        try:
                                            if data.decode("utf-8") == "stop":
                                                f.close()
                                                break
                                        except:
                                            pass 
                                        f.write(data)
                                break
                            elif test[0] == "#50#":
                                break

    def up_file(self):
        if self.test_mode:
            test = self.path_fichier_envoi.split("/")[-1]
            tempo = self.path_fichier_envoi
            self.connexion_server_local.send(pickle.dumps(["#06#",test,int(getsize(tempo)*1.2)]))
            if isfile(tempo):
                f = open(tempo, 'rb')
                while True:
                    l = f.read(int(getsize(tempo)*1.2))
                    while (l):
                        self.connexion_server_local.send(l)
                        l = f.read(int(getsize(tempo)*1.2))
                    if not l:
                        sleep(2)
                        self.connexion_server_local.send(pickle.dumps(["#60#",""]))
                        f.close()
                        break
            else:
                self.connexion_server_local.send(pickle.dumps(["#60#",""]))
        if not self.test_mode:
            test = self.path_fichier_envoi.split("/")[-1]
            tempo = self.path_fichier_envoi
            self.connexion_server_distant.send(pickle.dumps(["#06#",test,int(getsize(tempo)*1.2)]))
            if isfile(tempo):
                
                self.connexion_server_distant.send(pickle.dumps(["#06#",test,int(getsize(tempo)*1.2)]))
                f = open(tempo, 'rb')
                while True:
                    l = f.read(int(getsize(tempo)*1.2))
                    while (l):
                        self.connexion_server_distant.send(l)
                        l = f.read(int(getsize(tempo)*1.2))
                    if not l:
                        self.connexion_server_distant.send("stop".encode("utf-8"))
                        f.close()
                        break
            else:
                self.connexion_server_distant.send(pickle.dumps(["#60#",""]))

    def actualiser_fonction(self):
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#02#",""]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#02#",""]))

    def nouveau_dossier(self):
        global fen_secondary
        fen_secondary = tkinter.Toplevel(class_="nom de fichier",master=self.fen)
        fen_secondary.geometry("300x300")
        tkinter.Label(fen_secondary,text="enter un nom de dossier :").pack()
        global text_entry
        text_entry = tkinter.Entry(fen_secondary,width=120)
        text_entry.pack()
        def validation():
            global nom_dossier
            nom_dossier = text_entry.get()
            if self.test_mode:
                self.connexion_server_local.send(pickle.dumps(["#07#",nom_dossier]))
            else:
                self.connexion_server_distant.send(pickle.dumps(["#07#",nom_dossier]))
            fen_secondary.destroy()
        tkinter.Button(fen_secondary,text="vallidez le nom du dossier",command=validation).pack()
        fen_secondary.mainloop()

    def suprimer_dossier_fonction(self):
        tempo = self.listbox.get(self.listbox.curselection())
        if self.test_mode:
            self.connexion_server_local.send(pickle.dumps(["#08#",tempo]))
        else:
            self.connexion_server_distant.send(pickle.dumps(["#08#",tempo]))

main()