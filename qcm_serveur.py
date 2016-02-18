# -*- coding: utf-8 -*-
#!/usr/bin/env python


import socket, sys, threading, time,random, numpy

# variables globales

# adresse IP et port utilises par le serveur
HOST = ""
PORT = int(sys.argv[1])

NOMBREJOUEUR = int(sys.argv[2])
dureemax = 120 # durée max question ; en secondes
pause = 3 # pause entre deux questions  ; en secondes

dict_clients = {}  # dictionnaire des connexions clients
dict_pseudos = {}  # dictionnaire des pseudos
dict_reponses = {}  # dictionnaire des reponses des clients
dict_scores = {} # dictionnaire des scores de la derniere question
dict_scores_total = {}



#########################################################################################################################
#REMPLISSAGE DU TABLEAU DES QUESTIONS/REPONSES                                      #
#########################################################################################################################
 
questions = open("questions.txt", "r")
lines = questions.read().split(',\n\n')


questions.close()
 
TAB_QUESTIONS=[]
questions_tot=[]
for i in range(0,len(lines)-1):
    if (i % 2) == 0:
        q= lines[i],lines[i+1]
        questions_tot.append(q)
indices=numpy.random.choice(len(questions_tot),5,replace=False)


for j in indices:
    TAB_QUESTIONS.append(questions_tot[j])


##########################################################################################################################
class ThreadClient(threading.Thread):
    '''derivation de classe pour gerer la connexion avec un client'''
    
    def __init__(self,conn):

        threading.Thread.__init__(self)
        self.connexion = conn
        
        # Memoriser la connexion dans le dictionnaire
        
        self.nom = self.getName() # identifiant du thread
        dict_clients[self.nom] = self.connexion
        dict_scores[self.nom] = 0
        dict_scores_total[self.nom] = 0
        
        print("Connexion du client", self.connexion.getpeername(),self.nom ,self.connexion)
        
        message = "Le QCM va commencer.\n"
        self.connexion.send(message)
        
        
    def run(self):
        
        # Choix du pseudo    
        nom_client_possible=["le président","Einstein","un ordinateur"]
        nom_init=random.choice(nom_client_possible)
        self.connexion.send(b"Tu n'es pas " +str(nom_init) +", mais tu vas peut-etre gagner quand même...\n")
        # attente reponse client

        # pseudo = self.connexion.recv(4096)
        # pseudo = pseudo.decode(encoding='UTF-8')
        pseudo = ""
        while(pseudo==""):
            message = self.connexion.recv(4096)
            if(message[0:3]=="@@@"):
                # Message Chat
                MessagePourTous(message[0:3]+"Anonymous: "+message[3:]) # Renvoi pseudo+message
            else:
                pseudo = message
        pseudo = pseudo.decode(encoding='UTF-8')


        
        dict_pseudos[self.nom] = pseudo
        
        print("Donc tu es", self.connexion.getpeername(),">", pseudo)
        
        message = b"Attente des autres clients...\n"
        self.connexion.send(message)
    
        # Reponse aux questions
       
        while True:
            
            try:
                # attente reponse client
                # reponse = self.connexion.recv(4096)
                # reponse = reponse.decode(encoding='UTF-8')
                reponse = ""
                while(reponse==""):
                    message = self.connexion.recv(4096)
                    if(message[0:3]=="@@@"):
                        # Message Chat
                        MessagePourTous(message[0:3]+pseudo+": "+message[3:]) # Renvoi pseudo+message
                    else:
                        reponse = message
                reponse = reponse.decode(encoding='UTF-8')

            except:
                # fin du thread
                break
                
            # on enregistre la premiere reponse
            # les suivantes sont ignorees
            if self.nom not in dict_reponses:
                dict_reponses[self.nom] = reponse, time.time()
                print("Reponse du client",self.nom,">",reponse)

        print("\nFin du thread",self.nom)
        self.connexion.close()


###################################################################################

def MessagePourTous(message):
    """ message du serveur vers tous les clients"""
    for client in dict_clients:
        dict_clients[client].send(bytes(message))

###################################################################################
# main        
        
# Initialisation du serveur
# Mise en place du socket avec les protocoles IPv4 et TCP
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print("La liaison du socket a l'adresse choisie a echoue.")
    sys.exit()
print("Serveur pret (port",PORT,") en attente de clients...")
mySocket.listen(5)


# len(dict_clients) -> nb de joueurs connectes

while len(dict_clients) < NOMBREJOUEUR:
    # Attente connexion nouveau client
    try:
        connexion, adresse = mySocket.accept()
    except:
        sys.exit()
    # Creer un nouvel objet thread pour gerer la connexion
    th = ThreadClient(connexion)
    # The entire Python program exits when no alive non-daemon threads are left
    th.setDaemon(1)
    th.start()
    

while len(dict_pseudos) < NOMBREJOUEUR:
    # on attend que tout le monde ait entre son pseudo
    pass


MessagePourTous("\nLa partie va commencer !\n")

# questions
index = 0
for question in TAB_QUESTIONS:
    index += 1
    MessagePourTous("\nNouvelle question dans " + str(pause) + " secondes...\n")
    time.sleep(pause)

    timedebut = time.time()
    timefin = timedebut + dureemax
    dict_reponses = {}  # liste des reponses des clients
    dict_scores = {}

    message = """--------------------
Question """ +str(index)
    message += question[0]
    message += """
Reponse > """
    MessagePourTous(message)
        
    while time.time() < timefin and len(dict_reponses) <  NOMBREJOUEUR:
         # on attend que tout le monde ait repondu
         # ou que le delai soit ecoule
         pass

    # resultats et scores
    bonnereponse = question[1]

    clientbonus = ""
    for client in dict_reponses:
        try:
            reponse = int(dict_reponses[client][0])

            if reponse == int(bonnereponse):
                # bonne reponse 2 pts

                dict_scores[client] = 2
                
                if clientbonus == "":
                    clientbonus = client
                else:
                    # comparaison des durees
                    if dict_reponses[client][1] < dict_reponses[clientbonus][1]:
                        clientbonus = client
                

            elif reponse != int(bonnereponse) and reponse != 0:
                # mauvaise reponse -1 pt
                dict_scores[client] = -1
                
            else:
                # reponse je ne sais pas 0 pt
                dict_scores[client] = 0
            
        except:
            # mauvaise reponse -1 pt
            dict_scores[client] = -1
            
        dict_scores_total[client] += dict_scores[client]    
                
    # bonus pour la premiere bonne reponse
    if clientbonus != "":
        dict_scores[clientbonus] += 1
        dict_scores_total[clientbonus] += 1


    message = """
Resultat :
Client       Score    Temps
"""

    for client in dict_reponses:
        duree = dict_reponses[client][1] - timedebut
        message += "%-10s  %3d pt    %3.2f\"\n"  %(dict_pseudos[client],dict_scores[client],duree)
    message +="""    
Total :
Client       Score
""" 

    for client in dict_scores_total:
        message += "%-10s  %3d pt\n"  %(dict_pseudos[client],dict_scores_total[client])

    MessagePourTous(message)

# Fin
MessagePourTous("\nFIN\nVous pouvez fermer l'application...\n")

# fermeture des sockets
for client in dict_clients:
    dict_clients[client].close()
    print("Deconnexion du socket", client)

input("\nAppuyer sur Entree pour quitter l'application...\n")
# fermeture des threads (daemon) et de l'application
