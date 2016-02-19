#################################################
#       ReadMe - projet Reseau : QCM            #
#################################################

Ce fichier est le read me du projet QCM :
Il décrit le mode d'emploi du jeu



MODE D'EMPLOI 
#############

# LANCER LE JEU :

Sur un premier terminal utiliser la ligne de commande :
python qcm_serveur.py 8000 nombre_joueur_max_souhaite

Ouvrir un second terminal ou plusieurs (selon le nombre de joueurs voulu) et y utiliser la commande :
python qcm_client.py

# INTERACTION AVEC LE TERMINAL
Sur la petite fenêtre affichée, rentrer le num de HOST et PORT et puis appuyer sur le bouton "Connexion au serveur" pour accéder à la fenêtre principale.

Sur la fenêtre principale:
1. Vous allez voir un message d'accueil du serveur,
2. Entrer votre nom (pseudo),
3. Attendre jusqu'à le nombre maximum de joueur soit atteint,
4. Si tout le monde est en ligne, vous pouvez commencer (vous allez tous commencer en même temps).

#REGLE DU JEU:
1. Une bonne réponse: 2 pts
2. Une réponse "Je ne sais pas": 0 pts
3. Une mauvaise réponse: -1 pts
Il faut que tout le monde ait répondu pour pouvoir passer à la question suivante.

Les joueurs peuvent interagir via la fenêtre de chat à leur disposition.

Bonne chance!
