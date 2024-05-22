ce projet permet d'avoir l'équivalent des fonctionnalité d'un explorateur de fichier et d'un terminale (seulement le retour des commande et leurs envoi par exemple la commande "nano" ne marchera pas) pour un serveur à distance

pour configurer les utlisateur il faut, 
en premier crée un fichier json qui contiendras tout les utilisateur d'un groupe en suite dans le json il vous faudrat saisir un dictionnaire comme suit:
admin.json : {
"user 1":["password","chemin d'accés limite ex: document","root (fonctionnalité en cours de dévelopement)"],
"user 2":["password","chemin d'accés limite ex: document","root (fonctionnalité en cours de dévelopement)"]
}
user.json : {
"user 1":["password","chemin d'accés limite ex: document","root (fonctionnalité en cours de dévelopement)"],
"user 2":["password","chemin d'accés limite ex: document","root (fonctionnalité en cours de dévelopement)"]
"user 3":["password","chemin d'accés limite ex: document","root (fonctionnalité en cours de dévelopement)"]
}
ensuite il faudrat tous les mettre dans le dossier du serveur nommé "user"

les client ne peuvent pour le moment pas bloquer la fonctionnalité d'envoyé des commandes ni leurs configuration
la fonctionnalité de redémarage à distance n'est pas encore implémenté
