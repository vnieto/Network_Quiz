#! /usr/bin/python
# -*- coding: utf-8 -*-
 
 
from Tkinter import *
from tkMessageBox import *
import random
 
import socket, threading, signal
 
## Gestion du Ctrl-C
def signal_handler(signal, frame):
    print 'Vous avez appuye sur Ctrl+C!'
    global CONNEXION 
    CONNEXION = False
    fenetreJeu.destroy
 
 
## Methode d'envoi des reponses et d'affichage dans la fenetre de jeu 
#appelee par le bouton d'envoi de messages  
class ThreadReception(threading.Thread):
    """objet thread gerant la reception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        ref_socket[0] = conn
        self.connexion = conn  # ref. du socket de connexion
              
    def run(self):
        while True:
            try:
                # en attente de reception
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.decode(encoding='UTF-8')
                
                ZoneReception.config(state=NORMAL)
                ZoneReception.insert(END,message_recu)
                # defilement vers le bas
                ZoneReception.yview_scroll(1,"pages")
                # lecture seule
                ZoneReception.config(state=DISABLED)
                
                if "FIN" in message_recu:
                    # fin du qcm
                    global CONNEXION
                    CONNEXION = False
                    
            except socket.error:
                pass
def envoyer():
    if CONNEXION:
        try:
            #on recupere le message (reponse ou pseudo) entre dans le cadre d'envoi :
            message = MESSAGE.get()
            #on vide le cadre d'envoi :
            MESSAGE.set("")
             
            #On affiche le message dans l'espace de reception (cadre blanc) :
            espaceRecep.config(state=NORMAL)
            espaceRecep.insert(END,message+"\n")
             
            # On remet l'espace de reception en lecture seule (= le joueur ne peut pas rentrer directementdui texte a cet endroit) :
            espaceRecep.config(state=DISABLED)
             
            # On remet le bouton d'envoi de messages en etat inutilisable
            boutonEnvoyer.configure(state = DISABLED)
             
            #activate les Radiobuttons
            C1.configure(state=NORMAL)
            C2.configure(state=NORMAL)
            C3.configure(state=NORMAL)
            C4.configure(state=NORMAL)
            boutonRepondre.configure(state=NORMAL)
 
            # On envoi le message  
            newSock[0].send(message)
        except socket.error:
            showerror('Erreur',"L'envoi du message a rencontre un probleme : %s"%e)
             
def repondre():
    if CONNEXION:
        try:
            message = v.get()
	    
            espaceRecep.config(state=NORMAL)
            espaceRecep.insert(END,message+"\n")
             
            # On remet l'espace de reception en lecture seule (= le joueur ne peut pas rentrer directementdui texte a cet endroit) :
            espaceRecep.config(state=DISABLED)
             
            # On envoye la reponse
            newSock[0].send(message)
             
            # deselectionner les Radiobutton
            C1.deselect()
            C2.deselect()
            C3.deselect()
            C4.deselect()
                 
        except socket.error:
            showerror('Erreur',"L'envoi de la reponse a rencontre un probleme : %s"%e)      
 
## Methode de connexion au serveur        
#appelee par le bouton de demande de connexion  
def ConnexionServeur():
    global CONNEXION
    # Mise en place de la connexion si elle n'existe pas encore : : 
    if CONNEXION == False:
        try:
            #creation d'une socket pour le client :
            sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockClient.connect((HOST.get(), PORT.get()))
             
            #On utilise un thread pour gerer la reception des messages du serveur (par exemple les questions)
            def fonction_thread(sock,num):
                #ce qui est fait dans le thread :
                while True: 
                    try:
                        # On stocke la socket pour pouvoir la reutiliser :
                        newSock[0]=sock
                        # On enregistre le message recu par la socket :
                        messageRecu = sock.recv(4096)
                        # On affiche le message recu dans l'espace de reception, on descend la partie de l'espace de reception affichee, et on le repasse en lecteure seule : 
                        espaceRecep.config(state=NORMAL)
                        espaceRecep.insert(END,messageRecu)
                        espaceRecep.yview_scroll(1,"pages")
                        espaceRecep.config(state=DISABLED)
 
                        #gestion de la demande de fin du qcm par le serveur :
                        if "FIN" in messageRecu:
                            global CONNEXION
                            CONNEXION = False
                            sock.shutdown(1)
                     
                    except socket.error,e:
                        showerror('Erreur','La fonctionnement du thread a rencontre un probleme : %s'%e)
 
        
            #On cree le thread qui utilise la fonction ci-dessus et on le demarre :
            threadReception = threading.Thread(group=None,target=fonction_thread,name=None,args=(sockClient,1),kwargs={})
 
            threadReception.start()
 
            #La connexion est maintenant etablie :
            CONNEXION = True
            #On rend le bouton d'envoi utilisable et le bouton de demande de connexion inutilisable
            boutonEnvoyer.configure(state = NORMAL)
            boutonConnexion.configure(state = DISABLED)
             
        except socket.error, e:
            showerror('Erreur','La connexion au serveur a rencontre un probleme : %s'%e)
         
         
      
 
################################################################
#               DEBUT DU PROGRAMME
################################################################
 
#La connexion n'est pas encore etablie :
CONNEXION = False
#On cree une liste qui va stocker la socket utilisee pour communiquer avec le serveur :
newSock={} 
 
# On cree la fenetre principale :
fenetreJeu = Tk()
fenetreJeu.title('Questionnaire')
 
#On cree les differentes zones de la fenetre :
## cadreServeur : parametres du serveur
cadreServeur = Frame(fenetreJeu,borderwidth=2,relief=RAISED, background = "#A4F9F2")
 
#Definition de l'adresse de l'hote
Label(cadreServeur, text = "Hôte :").grid(row=0,column=0,padx=5,pady=5,sticky=W)
HOST = StringVar()
#valeur par defaut : jeu en local
HOST.set('127.0.0.1') 
Entry(cadreServeur, textvariable= HOST).grid(row=0,column=1,padx=5,pady=5)
 
#Definition du port utilise
Label(cadreServeur, text = "Port :").grid(row=1,column=0,padx=5,pady=5,sticky=W)
PORT = IntVar()
#valeur par defaut : 8000
PORT.set(8000)
Entry(cadreServeur, textvariable= PORT).grid(row=1,column=1,padx=5,pady=5)
 
#bouton pour la demande de connexion au serveur :
boutonConnexion = Button(cadreServeur, text ='Connexion au serveur',activebackground="#088A29", activeforeground = "#2EFEF7", background = "#2E64FE", disabledforeground ="#6E6E6E", command=ConnexionServeur)
boutonConnexion.grid(row=0,column=2,rowspan=2,padx=5,pady=5)
 
cadreServeur.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)
 
 
## cadreReception : reception et affichage des messages (pseudo, questions, reponses, resultats ...) (zone de texte et scrollbar)
cadreReception = Frame(fenetreJeu,borderwidth=2,relief=RAISED, background = "#A9F5BC")
 
# zone de texte (ici, zone d'affichage car elle est maintenue en lecture seule) :
espaceRecep = Text(cadreReception,width =80, height =15,state=DISABLED)
espaceRecep.grid(row=0,column=0,padx=5,pady=5)
#scrollbar :
scroll = Scrollbar(cadreReception, command = espaceRecep.yview, background = "#2EFE2E")
espaceRecep.configure(yscrollcommand = scroll.set)
scroll.grid(row=0,column=1,padx=5,pady=5,sticky=E+S+N)
 
cadreReception.grid(row=0,column=2,padx=5,pady=5)
 
## cadreEnvoi : envoi de messages au serveur (zone d'entree de texte et bouton d'envoi)
cadreEnvoi = Frame(fenetreJeu,borderwidth=2,relief=RAISED,background = "#E1F5A9")
 
#Checkbox pour les reponse
v = StringVar()
C1 = Radiobutton(cadreEnvoi, text = "1", variable = v, value="1", background = "#FE2E64", foreground = "#01DF01", state=DISABLED)
C1.grid(row=0, column=2)
C2 = Radiobutton(cadreEnvoi, text = "2", variable = v, value="2", background = "#FE2E64", foreground = "#01DF01", state=DISABLED)
C2.grid(row=0, column=3)
C3 = Radiobutton(cadreEnvoi, text = "3", variable = v, value="3",background = "#FE2E64", foreground = "#01DF01", state=DISABLED)
C3.grid(row=0, column=4)
C4 = Radiobutton(cadreEnvoi, text = "0", variable = v, value="0",background = "#FE2E64", foreground = "#01DF01", state=DISABLED)
C4.grid(row=0, column=5, columnspan= 3)
  
#bouton d'envoi de la reponse
boutonRepondre = Button(cadreEnvoi, text ='Repondre', command = repondre,state=DISABLED, activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E", background = "#FFBF00")
boutonRepondre.grid(row=0, column=8,padx=15)
 
#on stocke le message tape dans la variable MESSAGE :
MESSAGE = StringVar()
MESSAGE.set("Ton nom ici, stp")
Entry(cadreEnvoi, textvariable= MESSAGE).grid(row=0,column=0,padx=5,pady=5)
 
#bouton d'envoi du message
boutonEnvoyer = Button(cadreEnvoi, text ='Envoyer', command = envoyer, activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E", background = "#FFBF00", state=DISABLED)
boutonEnvoyer.grid(row=1,column=1,padx=5,pady=5,)
 
cadreEnvoi.grid(row=3,column=0,padx=5,pady=5,sticky=W+E)
 
#gestion du ctrl-C
signal.signal(signal.SIGINT, signal_handler)
#Affichage de la fenetre graphique
fenetreJeu.mainloop()
