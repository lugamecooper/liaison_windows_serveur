from socket import socket,AF_INET,SOCK_STREAM
from _thread import start_new_thread
from json import load,dump
import tkinter
from pickle import loads,dumps
from time import sleep
from tkinter.filedialog import askdirectory,askopenfile
from os.path import join,getsize,isfile,split
from re import findall

class main:
    def __init__(self) -> None:
        self.config = load(open(join(split(__file__)[0],"config.json")))
        start_new_thread(self.connexion_distant_thread,())
        start_new_thread(self.connexion_local_thread,())

        self.exit_test = False
        self.test_mode = None
        self.message_local = None
        self.message_distant = None
        self.path_down = None
        self.path_fichier_envoi = None
        self.file_size = None
        self.connected = False

        self.fen = tkinter.Tk(className="client_liaison_windows_serveur")
        self.fen.geometry(f"{self.fen.winfo_screenwidth()}x{self.fen.winfo_screenheight()}")
        self.fen.state("zoomed")

        self.menu_bar = tkinter.Menu(self.fen)
        self.menu_connection = tkinter.Menu(self.menu_bar,tearoff=0)
        self.menu_connection.add_command(label="connexion_distance",command=self.connexion_distance)
        self.menu_connection.add_command(label="connexion_local",command=self.connexion_local)
        self.menu_bar.add_cascade(label="menu connection",menu=self.menu_connection)

        self.menu_configuration = tkinter.Menu(self.menu_bar,tearoff=0)
        self.menu_configuration.add_command(label="configurer les adresses ip",command=self.configuration_config)
        self.menu_bar.add_cascade(label="menu configuration",menu=self.menu_configuration)
        
        self.fen.config(menu=self.menu_bar)

        self.body = tkinter.Frame(self.fen)

        self.affichage_init()

        self.body.pack()

        self.fen.mainloop()

        while True:
            if self.exit_test:
                exit()
            try:
                self.fen.configure()
            except:
                exit()

    def affichage_init(self):
        self.label_init = tkinter.Label(self.body,text="séléctioner une option de connection")
        self.label_init.pack()

    def login(self):
        if self.test_mode:
            self.message_config = self.message_local_config
        else:
            self.message_config = self.message_distant_config
        self.frame_login = tkinter.Frame(self.fen)
        self.string_var = tkinter.StringVar()
        self.string_var.set(self.message_config[4][0])
        self.login_menu_dropdown = tkinter.OptionMenu(self.frame_login,self.string_var,*self.message_config[4])

        self.frame_login_entry = tkinter.Frame(self.frame_login)
        self.login_label = tkinter.Label(self.frame_login_entry,text="nom d'utilisateur")
        self.login_entry = tkinter.Entry(self.frame_login_entry,width=40)

        self.frame_password_entry = tkinter.Frame(self.frame_login)
        self.login_password_label = tkinter.Label(self.frame_password_entry,text="mots de passe")
        self.password_entry = tkinter.Entry(self.frame_password_entry,width=40)

        self.login_menu_dropdown.pack()

        self.login_label.pack(side="top",anchor="nw")
        self.login_entry.pack(side="top",anchor="ne")
        self.frame_login_entry.pack()

        self.login_password_label.pack(side="top",anchor="nw")
        self.frame_password_entry.pack(side="top",anchor="ne")
        self.password_entry.pack()
        self.boutton_login = tkinter.Button(self.frame_login,text="se connecter",command=self.send_login).pack() # faire la fonction de connexion
        self.label_login = tkinter.Label(self.frame_login,text="")
        self.label_login.pack()
        self.frame_login.pack()

    def send_login(self):
        if self.test_mode:
            server = self.connexion_server_local
        else:
            server = self.connexion_server_distant
        server.send(dumps(["#81#",{"user":self.login_entry.get(),"password":self.password_entry.get()},self.string_var.get()]))

    def connexion_distance(self):
        self.label_init.destroy()
        self.test_mode = 0
        if self.message_distant_config[4] == None:
            self.commun("distante")
        else:
            self.login()

    def connexion_local(self):
        self.label_init.destroy()
        self.test_mode = 1
        if self.message_local_config[4] == None:
            self.commun("local")
        else:
            self.login()

    def commun(self,para):
        self.body.destroy()
        self.fen.update()
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
            self.connexion_server_local.send(dumps(["#02#"]))
        else:
            self.connexion_server_distant.send(dumps(["#02#"]))
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
                self.message_local = loads(self.connexion_server_local.recv(4096))
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
                elif self.message_local[0] == "#00#":
                    self.message_local_config = self.message_local
                elif self.message_local[0] == "#99#":
                    self.exit()
                elif self.message_local[0] == "#81#":
                    self.connected = self.message_local[1]
                    if self.connected:
                        self.frame_login.destroy()
                        self.fen.update()
                        if self.test_mode:
                            self.commun("local")
                        else:
                            self.commun("distante")
                    else:
                        self.label_login.config(text="connexion échoué")
                        self.frame_login.update()
                else:
                    pass

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
                self.message_distant = loads(self.connexion_server_distant.recv(1024))
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
                elif self.message_distant[0] == "#00#":
                    self.message_distant_config = self.message_distant
                elif self.message_distant[0] == "#99#":
                    self.exit()
                elif self.message_distant[0] == "#81#":
                    self.connected = self.message_distant[1]
                    if self.connected:
                        self.frame_login.destroy()
                        self.fen.update()
                        if self.test_mode:
                            self.commun("local")
                        else:
                            self.commun("distante")
                    else:
                        self.label_login.config(text="connexion échoué")
                        self.frame_login.update()

    def envoi_commande(self):
        if self.test_mode:
            self.connexion_server_local.send(dumps(["#01#",self.saisie_commande.get()]))
        else:
            self.connexion_server_distant.send(dumps(["#01#",self.saisie_commande.get()]))

    def avance_fichier(self):
        if self.test_mode:
            self.connexion_server_local.send(dumps(["#03#",self.listbox.get(self.listbox.curselection())]))
        else:
            self.connexion_server_distant.send(dumps(["#03#",self.listbox.get(self.listbox.curselection())]))

    def recul_fichier(self):
        if self.test_mode:
            self.connexion_server_local.send(dumps(["#04#"]))
        else:
            self.connexion_server_distant.send(dumps(["#04#",]))

    def selectionner_recup_fichier(self):
        test = askdirectory(title="séléctionner le dossier pour le téléchargement", initialdir=self.path_down)
        if test:
            self.path_down = test
            self.select_folder.config(text=f"changer de dossier pour le téléchargement\ndossier actuelle : '{self.path_down}'")
            self.select_folder.update()

    def selectionner_envoi_fichier(self):
        test = askopenfile(title="séléctionner le fichier à envoyer")
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
                    client.send(dumps(["#05#",self.listbox.get(self.listbox.curselection())]))
                    while True:
                        test = self.message_local
                        if test:
                            if test[0] == "#05#":
                                with open(join(self.path_down,test[1]), 'wb') as f:
                                        data = client.recv(int(test[2]))
                                        try:
                                            if loads(data) == "stop":
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
                    client.send(dumps(["#05#",self.listbox.get(self.listbox.curselection())]))
                    while True:
                        test = self.message_local
                        if test:
                            if test[0] == "#05#":
                                with open(join(self.path_down,test[1]), 'wb') as f:
                                        data = client.recv(int(test[2]))
                                        try:
                                            if loads(data) == "stop":
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
            self.connexion_server_local.send(dumps(["#06#",test,int(getsize(tempo)*1.2)]))
            if isfile(tempo):
                f = open(tempo, 'rb')
                while True:
                    l = f.read(int(getsize(tempo)*1.2))
                    while (l):
                        self.connexion_server_local.send(l)
                        l = f.read(int(getsize(tempo)*1.2))
                    if not l:
                        sleep(2)
                        self.connexion_server_local.send(dumps(["#60#",""]))
                        f.close()
                        break
            else:
                self.connexion_server_local.send(dumps(["#60#",""]))
        if not self.test_mode:
            test = self.path_fichier_envoi.split("/")[-1]
            tempo = self.path_fichier_envoi
            self.connexion_server_distant.send(dumps(["#06#",test,int(getsize(tempo)*1.2)]))
            if isfile(tempo):
                self.connexion_server_distant.send(dumps(["#06#",test,int(getsize(tempo)*1.2)]))
                f = open(tempo, 'rb')
                while True:
                    l = f.read(int(getsize(tempo)*1.2))
                    while (l):
                        self.connexion_server_distant.send(l)
                        l = f.read(int(getsize(tempo)*1.2))
                    if not l:
                        self.connexion_server_distant.send(dumps("stop"))
                        f.close()
                        break
            else:
                self.connexion_server_distant.send(dumps(["#60#",""]))

    def actualiser_fonction(self):
        if self.test_mode:
            self.connexion_server_local.send(dumps(["#02#",""]))
        else:
            self.connexion_server_distant.send(dumps(["#02#",""]))

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
                self.connexion_server_local.send(dumps(["#07#",nom_dossier]))
            else:
                self.connexion_server_distant.send(dumps(["#07#",nom_dossier]))
            fen_secondary.destroy()
        tkinter.Button(fen_secondary,text="vallidez le nom du dossier",command=validation).pack()
        fen_secondary.mainloop()

    def suprimer_dossier_fonction(self):
        tempo = self.listbox.get(self.listbox.curselection())
        if self.test_mode:
            self.connexion_server_local.send(dumps(["#08#",tempo]))
        else:
            self.connexion_server_distant.send(dumps(["#08#",tempo]))

    def configuration_config(self):
        self.frame_config = tkinter.Toplevel(self.fen,class_="configurateur")
        self.frame_config.geometry("650x500")

        self.frame_local = tkinter.Frame(self.frame_config)
        self.frame_distant = tkinter.Frame(self.frame_config)

        self.label_local = tkinter.Label(self.frame_local,text=f"ip local : {self.config[0]}\nport local : {self.config[1]}")
        self.frame_config_local_1 = tkinter.Frame(self.frame_local)
        self.label_local_1 = tkinter.Label(self.frame_config_local_1, text="ip : ")
        self.entry_local_1 = tkinter.Entry(self.frame_config_local_1,width=40)
        self.bouton_local_1 = tkinter.Button(self.frame_config_local_1,text="vallidez l'ip",command=self.config_local_ip)

        self.frame_config_local_2 = tkinter.Frame(self.frame_local)
        self.label_local_2 = tkinter.Label(self.frame_config_local_2, text="port : ")
        self.entry_local_2 = tkinter.Entry(self.frame_config_local_2,width=40)
        self.bouton_local_2 = tkinter.Button(self.frame_config_local_2,text="vallidez le port",command=self.config_local_port)

        self.label_local.pack(side="top",anchor="n")

        self.frame_config_local_1.pack(side="top",anchor="n")
        
        self.label_local_1.pack(side="left",anchor="n")
        self.entry_local_1.pack(side="top",anchor="n")
        self.bouton_local_1.pack(side="right",anchor="n")

        self.frame_config_local_2.pack(side="top",anchor="n")
        self.label_local_2.pack(side="left",anchor="n")
        self.entry_local_2.pack(side="top",anchor="n")
        self.bouton_local_2.pack(side="right",anchor="n")

        self.label_distant = tkinter.Label(self.frame_distant,text=f"ip distant : {self.config[2]}\nport distant : {self.config[3]}")
        self.frame_config_distant_1 = tkinter.Frame(self.frame_distant)
        self.label_distant_1 = tkinter.Label(self.frame_config_distant_1, text="ip : ")
        self.entry_distant_1 = tkinter.Entry(self.frame_config_distant_1,width=40)
        self.bouton_distant_1 = tkinter.Button(self.frame_config_distant_1,text="vallidez l'ip",command=self.config_distant_ip)

        self.frame_config_distant_2 = tkinter.Frame(self.frame_distant)
        self.label_distant_2 = tkinter.Label(self.frame_config_distant_2, text="port : ")
        self.entry_distant_2 = tkinter.Entry(self.frame_config_distant_2,width=40)
        self.bouton_distant_2 = tkinter.Button(self.frame_config_distant_2,text="vallidez le port",command=self.config_distant_port)

        self.label_warning = tkinter.Label(self.frame_config,font=("Arial", 12) ,text="attention la modification des ports peut entrainer des erreurs inentendus\nwarning modify the port can cause some isues")

        self.label_distant.pack(side="top",anchor="n")
        
        self.frame_config_distant_1.pack(side="top",anchor="n")
        self.label_distant_1.pack(side="left",anchor="n")
        self.entry_distant_1.pack(side="top",anchor="n")
        self.bouton_distant_1.pack(side="right",anchor="n")

        self.frame_config_distant_2.pack(side="top",anchor="n")
        self.label_distant_2.pack(side="left",anchor="n")
        self.entry_distant_2.pack(side="top",anchor="n")
        self.bouton_distant_2.pack(side="right",anchor="n")

        self.label_warning.pack(side="bottom",anchor="center")

        self.frame_local.pack(side="left")
        self.frame_distant.pack(side="right")

        self.frame_config.mainloop()

    def config_distant_ip(self):
        if self.entry_distant_1.get():
            test = True
            try:
                tempo = findall(r"(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})",self.entry_distant_1.get())[0]
            except:
                test = False
                tempo = []
            for i in tempo:
                try:
                    i = int(i)
                    if i < 256 and i >= 0:
                        pass
                    else:
                        test = False
                except:
                    pass
            if test:
                self.config[2] = ".".join(tempo)
                dump(self.config,open(join(split(__file__)[0],"config.json"),"w"))
                self.label_distant.config(text=f"ip distant : {self.config[2]}\nport distant : {self.config[3]}")
                self.frame_distant.update()

    def config_local_ip(self):
        if self.entry_local_1.get():
            test = True
            try:
                tempo = findall(r"(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})",self.entry_local_1.get())[0]
            except:
                test = False
                tempo = []
            for i in tempo:
                try:
                    i = int(i)
                    if i < 256 and i >= 0:
                        pass
                    else:
                        test = False
                except:
                    pass
            if test:
                self.config[0] = ".".join(tempo)
                dump(self.config,open(join(split(__file__)[0],"config.json"),"w"))
                self.label_local.config(text=f"ip local : {self.config[0]}\nport local : {self.config[1]}")
                self.frame_local.update()

    def config_distant_port(self):
        try:
            if self.entry_distant_2.get():
                self.config[4] = int(self.entry_distant_2)
                dump(self.config,open(join(split(__file__)[0],"config.json"),"w"))
                self.label_distant.config(text=f"ip distant : {self.config[2]}\nport distant : {self.config[3]}")
                self.frame_local.update()
        except:
            pass

    def config_local_port(self):
        try:
            if self.entry_local_2.get():
                self.config[1] = int(self.entry_local_2)
                dump(self.config,open(join(split(__file__)[0],"config.json"),"w"))
                self.label_distant.config(text=f"ip local : {self.config[0]}\nport local : {self.config[1]}")
                self.frame_local.update()
        except:
            pass

    def exit(self):
        self.fen.quit()
        sleep(0.2)
        fen_exit = tkinter.Tk(className="message serveur")
        tkinter.Label(fen_exit,text="le serveur à redémarer").pack()
        tkinter.Button(fen_exit,text="quitter",command=self.test_exit).pack()
        fen_exit.geometry("300x300")
        fen_exit.mainloop()

    def test_exit(self):
        self.exit_test = True
        exit()

main()