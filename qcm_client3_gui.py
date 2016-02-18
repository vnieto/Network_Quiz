#! /usr/bin/python
# -*- coding: utf-8 -*-


import Tkinter as tk
from tkMessageBox import *
import random
import socket,sys, threading, signal

#################### cA MARCHE??? ###########################""

def signal_handler(signal, frame):
    print 'Vous avez appuye sur Ctrl+C!'
    global CONNEXION 
    CONNEXION = False
    sys.exit(0)
 


class ThreadReception(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        ref_socket[0] = conn
        self.connexion = conn  # réf. du socket de connexion
              
    def run(self):
        while True:
            try:
                # en attente de réception
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.decode(encoding='UTF-8')
                
                ZoneReception.config(state=NORMAL)
                ZoneReception.insert(END,message_recu)
                # défilement vers le bas
                ZoneReception.yview_scroll(1,"pages")
                # lecture seule
                ZoneReception.config(state=DISABLED)
                
                if "FIN" in message_recu:
                    # fin du qcm
                    global CONNEXION
                    CONNEXION = False
                    
            except socket.error:
                pass

class fen1:
    def __init__(self,master):
        self.master=master

        self.master.title('Information')
         
        #On créé les différentes zones de la fenêtre :
        ## cadreServeur : paramètres du serveur
        self.cadreServeur = tk.Frame(self.master,borderwidth=2,relief=tk.GROOVE, background = "#A4F9F2")
        self.cadreServeur.pack(side=tk.LEFT,padx=60,pady=60) 
        self.HOST = tk.StringVar()
        self.HOST.set('127.0.0.1') 
        tk.Entry(self.cadreServeur, textvariable= self.HOST).grid(row=0,column=1,padx=5,pady=5)
        self.PORT = tk.IntVar()
        #valeur par défaut : 8000
        self.PORT.set(8000)
        tk.Entry(self.cadreServeur, textvariable= self.PORT).grid(row=1,column=1,padx=5,pady=5)


        #Définition de l'adresse de l'hote
        tk.Label(self.cadreServeur, text = "Hôte :").grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)

         
        #Définition du port utilisé
        tk.Label(self.cadreServeur, text = "Port :").grid(row=1,column=0,padx=5,pady=5,sticky=tk.W)


        self.boutonConnexion = tk.Button(self.cadreServeur, text ='Connexion au serveur',activebackground="#088A29", activeforeground = "#2EFEF7", background = "#2E64FE", disabledforeground ="#6E6E6E", command=self.new_window)
        self.boutonConnexion.grid(row=0,column=2,rowspan=2,padx=5,pady=5)
 
    def new_window(self):
        
        self.newWindow = tk.Toplevel(self.master)
        temp = fen2(self.newWindow)
        conn(self,temp)
        self.app=temp
        self.boutonConnexion.config(state=tk.DISABLED)

  

class fen2:
    def __init__(self,master):
        self.master=master
        self.master.title('Quiz')

        ##########################################################################  
        #-----------------------------PREMIER CADRE------------------------------#
        ##########################################################################  


        self.cadreEnvoi = tk.Frame(self.master,borderwidth=1,relief=tk.RAISED,background = "#E1F5A9")
 
        self.MESSAGE = tk.StringVar()
        self.MESSAGE.set("Ton nom ici, stp")
        tk.Entry(self.cadreEnvoi, textvariable= self.MESSAGE).grid(row=0,column=0,padx=5,pady=5)



        self.boutonEnvoyer = tk.Button(self.cadreEnvoi, text ='Envoyer', command = self.envoyer, activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E", background = "#FFBF00", state=tk.NORMAL)
        self.boutonEnvoyer.grid(row=0,column=1,padx=5,pady=5,)
         
        self.cadreEnvoi.grid(row=0,column=0,padx=5,pady=5, columnspan=2)


        ##########################################################################  
        #----------------------------DEUXIEME CADRE------------------------------#
        ##########################################################################  

        self.cadrebouttons=tk.Frame(self.master,  borderwidth=2, relief=tk.RAISED, background="#E1F5A9",width =60, height =15)

        
        self.C1 = tk.Button(self.cadrebouttons, width =25, height =5, text="1", command= lambda: self.repondre(self.C1.cget('text')), activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E",background="#FE2E64", state=tk.DISABLED)
        self.C1.grid(row=0, column=0)
        self.C2 = tk.Button(self.cadrebouttons, width =25, height =5,text = "2", command= lambda: self.repondre(self.C2.cget('text')), activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E",background = "#FE2E64", state=tk.DISABLED)
        self.C2.grid(row=0, column=1)
        self.C3 = tk.Button(self.cadrebouttons, width =25, height =5,text = "3", command= lambda: self.repondre(self.C3.cget('text')), activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E",background = "#FE2E64", state=tk.DISABLED)
        self.C3.grid(row=1, column=0)
        self.C4 = tk.Button(self.cadrebouttons, width =25, height =5,text = "0", command= lambda: self.repondre(self.C4.cget('text')),  activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E",background = "#FE2E64", state=tk.DISABLED)
        self.C4.grid(row=1, column=1)


        self.cadrebouttons.grid(row=3, column=0,rowspan=2, columnspan=2)

        ##########################################################################  
        #---------------------------TROISIEME CADRE------------------------------#
        ##########################################################################  




        self.cadreReception = tk.Frame(self.master,borderwidth=2,relief=tk.RAISED, background = "#A9F5BC")
        self.espaceRecep = tk.Text(self.cadreReception,width =60, height =15,state=tk.DISABLED)
        self.espaceRecep.grid(row=0,column=0,padx=5,pady=5)
        self.scroll = tk.Scrollbar(self.cadreReception, command = self.espaceRecep.yview, background = "#2EFE2E")
        self.espaceRecep.configure(yscrollcommand = self.scroll.set)
        self.scroll.grid(row=0,column=1,padx=5,pady=5,sticky=tk.E+tk.S+tk.N)
        self.cadreReception.grid(row=1,column=0,padx=5,pady=5,rowspan=2,columnspan=2)

        ##########################################################################  
        #---------------------------QUATRIEME CADRE------------------------------#
        ##########################################################################  

        #affichage des clients !!



        # self.cadreClients = tk.Frame(self.master,borderwidth=2,relief=tk.RAISED, background = "#A9F5BC")
        # self.liste = tk.Text(self.cadreClients,width =40, height =35,state=tk.DISABLED)
        # self.liste.grid(row=0,column=0,padx=5,pady=5)
        # self.scroll2 = tk.Scrollbar(self.cadreClients, command = self.liste.yview, background = "#2EFE2E")
        # self.liste.configure(yscrollcommand = self.scroll2.set)
        # self.scroll2.grid(row=0,column=1,padx=5,pady=5,sticky=tk.E+tk.S+tk.N)
        # self.cadreClients.grid(row=0,column=3,padx=5,pady=5,rowspan=4)



        ##########################################################################  
        #--------------------------- CINQUIEME CADRE-----------------------------#
        ##########################################################################  

        #chat???? 
        self.chat = tk.Frame(self.master,borderwidth=2,relief=tk.RAISED, background = "#A9F5BC")
        self.cc = tk.Text(self.chat,width =40, height =30,state=tk.DISABLED)
        self.cc.grid(row=0,column=0,padx=5,pady=5)
        self.scroll3 = tk.Scrollbar(self.chat, command = self.cc.yview, background = "#2EFE2E")
        self.cc.configure(yscrollcommand = self.scroll3.set)
        self.scroll3.grid(row=0,column=1,padx=5,pady=5,sticky=tk.E+tk.S+tk.N)
        self.chat.grid(row=0,column=4,padx=5,pady=5,rowspan=4)


        self.ecrire = tk.Frame(self.master,height=20,borderwidth=1,relief=tk.RAISED,background = "#E1F5A9")
 
        self.ME = tk.StringVar()
        self.ME.set("Ecris ici")
        tk.Entry(self.ecrire, textvariable= self.ME).grid(row=0,column=0,padx=5,pady=5)



        self.boutEnvoyer = tk.Button(self.ecrire, text ='Envoyer', command = self.envoyer_chat, activebackground="#088A29", activeforeground = "#FBFF03",disabledforeground ="#6E6E6E", background = "#FFBF00", state=tk.NORMAL)
        self.boutEnvoyer.grid(row=0,column=1,padx=5,pady=5,)
         
        self.ecrire.grid(row=4,column=4,padx=5,pady=5)


    def envoyer_chat(self):
        if CONNEXION:
            try:
                #on récupère le message entré dans le cadre d'envoi :
                message = "@@@"+self.ME.get()
                #on vide le cadre d'envoi :
                self.ME.set("")
                 
                # #On affiche le message dans l'espace de récéption (cadre blanc) :
                # self.cc.config(state=tk.NORMAL)
                # self.cc.insert(tk.END,message+"\n")
                # # On remet l'espace de récéption en lecture seule (= le joueur ne peut pas rentrer directementdui texte à cet endroit) :
                # self.cc.config(state=tk.DISABLED)
                 
                # On remet le bouton d'envoi de messages en état inutilisable
                # self.boutonEnvoyer.configure(state = tk.DISABLED)
                 
                #activate les Radiobuttons
                # self.C1.configure(state=tk.NORMAL)
                # self.C2.configure(state=tk.NORMAL)
                # self.C3.configure(state=tk.NORMAL)
                # self.C4.configure(state=tk.NORMAL)
                #self.boutonRepondre.configure(state=tk.NORMAL)
     
                # On envoi le message  
                newSock[0].send(message)
            except socket.error:
                showerror('Erreur',"L'envoi du message a rencontré un problème : %s"%e)

    def envoyer(self):
        if CONNEXION:
            try:
                #on récupère le message (réponse ou pseudo) entré dans le cadre d'envoi :
                message = self.MESSAGE.get()
                #on vide le cadre d'envoi :
                self.MESSAGE.set("")
                 
                #On affiche le message dans l'espace de récéption (cadre blanc) :
                self.espaceRecep.config(state=tk.NORMAL)
                self.espaceRecep.insert(tk.END,message+"\n")
                 
                # On remet l'espace de récéption en lecture seule (= le joueur ne peut pas rentrer directementdui texte à cet endroit) :
                self.espaceRecep.config(state=tk.DISABLED)
                 
                # On remet le bouton d'envoi de messages en état inutilisable
                self.boutonEnvoyer.configure(state = tk.DISABLED)
                 
                #activate les Radiobuttons
                self.C1.configure(state=tk.NORMAL)
                self.C2.configure(state=tk.NORMAL)
                self.C3.configure(state=tk.NORMAL)
                self.C4.configure(state=tk.NORMAL)
                #self.boutonRepondre.configure(state=tk.NORMAL)
     
                # On envoi le message  
                newSock[0].send(message)
            except socket.error:
                showerror('Erreur',"L'envoi du message a rencontré un problème : %s"%e)

    def repondre(self,t):
        if CONNEXION:
            try:
                message = t
                self.espaceRecep.config(state=tk.NORMAL)
                self.espaceRecep.insert(tk.END,message+"\n")
                 
                # On remet l'espace de récéption en lecture seule (= le joueur ne peut pas rentrer directementdui texte à cet endroit) :
                self.espaceRecep.config(state=tk.DISABLED)
                 
                # On envoye la réponse
                newSock[0].send(message)
                 
                # désélectionner les Radiobutton
                # self.C1.deselect()
                # self.C2.deselect()
                # self.C3.deselect()
                # self.C4.deselect()
                     
            except socket.error:
                showerror('Erreur',"L'envoi de la réponse a rencontré un problème : %s"%e)     

def conn(f1,f2):
    global CONNEXION
    # Mise en place de la connexion si elle n'existe pas encore : : 
    if CONNEXION == False:
        try:
            #création d'une socket pour le client :
            sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockClient.connect((f1.HOST.get(), f1.PORT.get()))

            def fonction_thread(sock,num):
                #ce qui est fait dans le thread :
                while True: 
                    try:
                        # On stocke la socket pour pouvoir la réutiliser :
                        newSock[0]=sock
                        # On enregistre le message reçu par la socket :
                        # messageRecu = sock.recv(4096)
                        messageRecu = ""
                        while(messageRecu==""):
                            message = sock.recv(4096)
                            if(message[0:3]=="@@@"):
                                # Message Chat
                                f2.cc.config(state=tk.NORMAL)
                                f2.cc.insert(tk.END,message[3:]+"\n")
                                f2.cc.yview_scroll(1,"pages")
                                f2.cc.config(state=tk.DISABLED)
                            else:
                                messageRecu = message
                        #messageRecu = messageRecu.decode(encoding='UTF-8')                        

                        # On affiche le message reçu dans l'espace de reception, on descend la partie de l'espace de récéption affichée, et on le repasse en lecteure seule : 
                        f2.espaceRecep.config(state=tk.NORMAL)
                        f2.espaceRecep.insert(tk.END,messageRecu)
                        f2.espaceRecep.yview_scroll(1,"pages")
                        f2.espaceRecep.config(state=tk.DISABLED)


                        #gestion de la demande de fin du qcm par le serveur :
                        if "FIN" in messageRecu:
                            global CONNEXION
                            CONNEXION = False
                            sock.shutdown(1)
                     
                    except socket.error,e:
                        showerror('Erreur','La fonctionnement du thread a rencontré un problème : %s'%e)

            # def fonction_thread_chat(sock,num):
            #     #ce qui est fait dans le thread :
            #     while True: 
            #         try:
            #             # On stocke la socket pour pouvoir la réutiliser :
            #             newSock[1]=sock
            #             # On enregistre le message reçu par la socket :
            #             messageRecu_chat = sock.recv(4096)
            #             # On affiche le message reçu dans l'espace de reception, on descend la partie de l'espace de récéption affichée, et on le repasse en lecteure seule : 
            #             f2.cc.config(state=tk.NORMAL)
            #             f2.cc.insert(tk.END,messageRecu_chat)
            #             f2.cc.yview_scroll(1,"pages")
            #             f2.cc.config(state=tk.DISABLED)
                     
            #         except socket.error,e:
            #             showerror('Erreur','La fonctionnement du thread a rencontré un problème : %s'%e)




            threadReception = threading.Thread(group=None,target=fonction_thread,name=None,args=(sockClient,1),kwargs={})

            threadReception.start()

            # threadReception_chat = threading.Thread(group=None,target=fonction_thread_chat,name=None,args=(sockClient,1),kwargs={})
            # threadReception_chat.start()

            #La connexion est maintenant établie :
            CONNEXION = True
            #On rend le bouton d'envoi utilisable et le bouton de demande de connexion inutilisable
         
        except socket.error, e:
            showerror('Erreur','La connexion au serveur a rencontré un problème : %s'%e)
            f2.master.destroy()
            f1.boutonConnexion.config(state=tk.NORMAL)





CONNEXION=False

newSock={}




def main(): 
    signal.signal(signal.SIGINT, signal_handler)
    root = tk.Tk()
    
    app = fen1(root)
    root.mainloop()



if __name__ == '__main__':
    main()


#SI PAS DE CONNEXION PAS DE FENETRE