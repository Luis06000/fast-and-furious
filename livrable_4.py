# importation des bibliotheques utiles au bon deroulement du programme
import tkinter as tk # affichage de la fenetre permettant de choisir le vehicule et ses options
from tkinter import ttk # importation des widgets supplementaires (volets deroulants)
import numpy as np # importation des methodes mathematiques(np.cos(), np.sin() ...)
import matplotlib.pyplot as plt # affichages des courbes
import matplotlib.image as mpimg # affichage des images
import time # marquer des temps d'arret
import sys # quitter le programme


class Parametres: # declaration de la classe servant a choisir les parametres de la simulation
    voiture = None      #| initialisation des variables de classe
    frottements = None  #| 
    options = None      #|
    partie = None       #|
    def __init__(self, voitures): # creation de la fonction principale, qui initialise les variables et autres attributs necessaires
        self.voitures = list(voitures.keys()) # recuperation des cles du dictionnaire afin d'avoir les modeles de voitures en string

        # Creation de la fenêtre principale
        self.fenetre = tk.Tk()
        self.fenetre.title("Choix des parametres")

        # Libelle pour le choix du modele de voiture
        voiture_label = tk.Label(self.fenetre, text="Modele de voiture :")
        voiture_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        # Creation de la variable de menu deroulant pour le choix du modele de voiture
        self.voiture_var = tk.StringVar(value=self.voitures[0])

        # Creation du menu deroulant pour le choix du modele de voiture
        self.voiture_combobox = ttk.Combobox(self.fenetre, textvariable=self.voiture_var, values=self.voitures)
        self.voiture_combobox.grid(row=0, column=1, padx=10, pady=5)

        # Libelle pour le choix des options
        options_label = tk.Label(self.fenetre, text="Choix des options :")
        options_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        # Creation de la variable de menu deroulant pour le choix des options
        self.options_var = tk.StringVar(value="Aucune option")

        # Creation du menu deroulant pour le choix des options
        self.options_combobox = ttk.Combobox(self.fenetre, textvariable=self.options_var, values=["Aucune option", "Nitro", "Jupe et ailerons", "Nitro + jupe et ailerons"])
        self.options_combobox.grid(row=2, column=1, padx=10, pady=5)            

        # Bouton de validation
        valider_button = tk.Button(self.fenetre, text="Valider", command=self.valider)
        valider_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Execution de la boucle principale
        self.fenetre.mainloop()

    def valider(self): # creation de la fonction permettant de recuperer et de traiter les valeurs selectionnees
        self.__class__.voiture = self.voiture_var.get() # recuperation de la voiture selectionnee
        self.__class__.options = self.options_var.get() # recuperation des options selectionnees

        # affichage des valeurs selectionnees
        print(f"Modele de voiture choisi : {self.__class__.voiture}")
        print(f"Options : {self.__class__.options}")
        self.fenetre.destroy() # fermeture de la fenetre de selection
        
        # verification des valeurs
        if self.__class__.options == 'Nitro' or self.__class__.options == 'Nitro + jupe et ailerons': 
            self.__init2__() # lancement de la deuxieme fenetre de selection
            
    def __init2__(self): # fonction permettant la creation de la seconde fenetre de selection
        # Creation de la seconde fenêtre
        self.fenetre2 = tk.Tk()
        self.fenetre2.title("Choix de la partie (nitro)")
            
        # Libelle pour le choix de la partie sur laquelle on applique le nitro
        partie_label = tk.Label(self.fenetre2, text="Partie du circuit :")
        partie_label.grid(row=2, column=0, padx=25, pady=5, sticky=tk.W)

        # Creation de la variable de menu deroulant pour le choix des options
        self.partie_var = tk.StringVar(value="pente")

        # Creation du menu deroulant pour le choix des options
        self.partie_combobox = ttk.Combobox(self.fenetre2, textvariable=self.partie_var, values=["pente", "looping", "arrivee"])
        self.partie_combobox.grid(row=2, column=1, padx=10, pady=5)
            
        # Bouton de validation
        valider_button_2 = tk.Button(self.fenetre2, text="Valider", command=self.valider_2)
        valider_button_2.grid(row=3, column=0, columnspan=2, pady=10)
        
    def valider_2(self): # creation de la fonction permettant la seconde validation
        self.__class__.partie = self.partie_var.get() # recuperation de la partie dans laquelle on appliquera le nitro
        print(f"Partie du circuit (Nitro) : {self.__class__.partie}") # affichage de la partie du circuit selectionnee
        self.fenetre2.destroy() # fermeture de la deuxieme fenetre

    def return_value(self): # fonction permettant de renvoyer les variables de classe necessaires pour la suite
        return self.__class__.voiture, self.__class__.frottements, self.__class__.options, self.__class__.partie # renvoie des valeurs


class  Simulation: # creation de la seconde classe, qui va effectuer toute la partie numerique (calculs et affichages)
    vitesse = None # variable de classe qui va stocker la vitesse
    temps = None # variable de classe qui va stocker le temps 
    def __init__(self, donnees, voiture, frottements, options): # creation de la fonction principale, qui initialise les variables et autres attributs necessaires
        self.donnees = donnees          # |  recuperation des donnees externes a la classe
        self.voiture = voiture          # |
        self.frottements = frottements  # |
        self.option = options           # |
        self.L = self.donnees['longueur'] #extraction des donnees des voiures
        self.S = self.donnees['largeur'] * self.L # calcul de la surface de la voiture
        if Parametres.options == 'Jupe et ailerons' or Parametres.options == 'Nitro + jupe et ailerons': # verification a propos de l'utilisation de la jupe et des ailes
            self.donnees['masse'] += 45                     # | modification des donnees conscernees
            self.donnees['Cz'] += self.donnees['Cz'] * 0.1  # |
            self.donnees['Cx'] -= self.donnees['Cx'] * 0.05 # |
            self.S += 0.8                                   # |
        self.g = 9.81                           # | recuperation des autres donnees 
        self.rho = 1.204                        # |
        self.mu = 0.1                           # |
        self.l=self.donnees['largeur']          # |
        self.h=self.donnees['hauteur']          # |
        self.m =self.donnees['masse']           # |
        self.Cx =self.donnees['Cx']             # |
        self.Cz =self.donnees['Cz']             # |
        self.aM =self.donnees['acceleration']   # |
        self.Ucp =self.donnees['Ucp']           # |
        self.Ucl =self.donnees['Ucl']           # |
        
        
        
    def incertitude(self, portion):
        if portion == 'pente':
            v = self.__class__.vitesse
            k = 2
            Ue = k * self.Ucp
            plage_de_valeurs = [v - Ue, v + Ue]
            return plage_de_valeurs
        elif portion == 'looping':
            v = self.__class__.vitesse
            k = 2
            Ue = k * self.Ucl
            plage_de_valeurs = [v - Ue, v + Ue]
            return plage_de_valeurs
        
    
    
    def vitesse_pente(self): # creation de la fonction ui va calculer la vitesse en bas de la pente
        Vn = 0                      # | initialisation des valeurs initiales
        distance = 0                # |
        self.pas = 0.005             # |
        self.__class__.temps = 0    # |
        if Parametres.partie == 'pente': # verification sur l'utilisation du nitro
            self.aM += self.aM * 0.3 # modification de la valeur de l'acceleration en consequence
    
        def pente_eul(Vn,distance,pas,temps): # creation de la fonction recursive
            if distance < 31: # condition initiale
                # equation de la vitesse
                Vn_1 = pas *((-self.rho * self.l * self.h * self.Cx * Vn**2 )/ (2*self.m) - self.mu * self.g + self.aM + self.g * np.sin(3.7*np.pi/180)) + Vn
                distance_New = Vn_1 * pas + distance #  ajustement de la valeur initiale (distance)
                New_temps = temps + pas # ajustement due la valeur initiale (temps)
                return pente_eul(Vn_1,distance_New,pas,New_temps) # appel de la fonction recursive
            else:                   # | une fois la distance de la pente parcourue
                return Vn, temps    # | on renvoie les valeurs dont nous avons besoin
            
        self.__class__.vitesse, self.__class__.temps = pente_eul(Vn,distance,self.pas,self.__class__.temps) # affectation des valeur renvoyees a nos variables de classe
        # affichage des valeurs du temps et de la vitesse arrondies au centieme
        print(f'La {self.voiture} est arrivee en bas de la pente en ', round(self.__class__.temps,2), ' secondes, a une vitesse de ', round(self.__class__.vitesse,2), "m/s. Avec l'incertitude, la vitesse sera comprise entre ", round(self.incertitude('pente')[0],2), " et ", round(self.incertitude('pente')[1],2)," m/s.")



    def vitesse_looping(self): # creation de la fonction qui calculera la vitesse dans le looping
        if Parametres.partie == 'looping': # verification sur l'utilisation du nitro
            self.aM += self.aM * 0.3 # modification de la valeur de l'acceleration en consequence
        
        theta = 0 # initialisation de l'angle a 0 radians
        v_vitesse = []  # | creation des tableaux qui vont stocker les valeurs necessaires a l'affichage
        v_temps = []    # |
        for i in range(3000): # boucle servant a parcourir le tour du looping
            # equation de la vitesse
            self.__class__.vitesse += ((-(0.5 * self.Cx * (self.l * self.h) * self.rho * self.__class__.vitesse**2) - (self.mu * (self.m * self.g * np.cos(theta) + (self.m * (self.__class__.vitesse**2) / 6))) - (self.m * self.g * np.sin(theta)) + self.m * self.aM) / self.m) * self.pas
            theta += (self.__class__.vitesse / 6) * self.pas # augmentation de la valeur de theta
            v_vitesse.append(self.__class__.vitesse)    # | ajout des valeurs de la vitesse
            v_temps.append(i * self.pas)                # | et du temps dans les tableaux
            if 3.145 > theta > 3.14 : # verification si la voiture se trouve en haut du looping
                print(f'La vitesse de la {self.voiture} en haut du looping est de',round(self.__class__.vitesse,2), 'm/s.') # affichage de la vitesse de la voiture en haut du looping
                if self.__class__.vitesse < 7.7: # comparaison a la vitesse minimale necessaire
                    print(f"La vitesse de la {self.voiture} est insuffisante pour passer le looping.") # affichage que la vitesse n'est pas suffisante en cas de besoin
                    sys.exit() # si la vitesse ne suffit pas, le programme s'arrete
            if theta >= 2 * np.pi: # verification si la voiture a complete le looping
                break # sortie de la fonction si le looping est complete
            
        plt.figure(figsize=(12, 6)) # cr&ation de la figure
        plt.subplot(1, 2, 1) # creation du sous graphique
        plt.plot(v_temps, v_vitesse, label='Vitesse (m/s)') # trace du graphique lineaire
        plt.xlabel('Temps (s)') # titre des l'axe des abscisses
        plt.ylabel('Vitesse (m/s)') # titre de l'axe des ordonnees
        plt.title('Vitesse en fonction du temps') # titre du graphique
        plt.grid() # affichage de la grille
        plt.legend() #affichage de la legende
        plt.tight_layout() # garantit l'innsertion du graphique dans l'espace disponible
        plt.show() # affichage final de la figure

        self.__class__.temps += i * self.pas # mise a jour du temps total
        # affichage des valeurs de la vitesse et du temps actuels
        print(f'La {self.voiture} est sortie du looping  ', round(self.__class__.temps,2), ' secondes apres son entree dans le circuit, a une vitesse de ', round(self.__class__.vitesse,2), "m/s. Avec l'incertitude, la vitesse sera comprise entre ",round(self.incertitude('looping')[0],2), " et ",round(self.incertitude('looping')[1],2)," m/s.")
            
    
    
    def vitesse_saut(self): # creation de la fonction qui calculera la vitesse dans le saut
        distance_y = 0 # | initialisation des valeurs initiales
        distance_x = 0 # | 
        def saut_eul(Vnx, Vny, distance_y, distance_x, pas, temps): # creation de la fonction recursive
            if distance_y > -1: # condition initiale
                # equation de la vitesse sur x et sur y
                Vn_1x = pas * ((-self.rho * self.l * self.h * self.Cx * Vnx**2) / (2 * self.m)) + Vnx 
                Vn_1y = pas * (((-self.rho * self.l * self.h * self.Cz * Vny**2) / (2 * self.m) - self.g)) + Vny
                New_temps = temps + pas # mise a jour du temps
                distance_y = distance_y + (Vn_1y) * pas # | mise a jour des distances
                distance_x = distance_x + (Vn_1x) * pas # |
                return saut_eul(Vn_1x, Vn_1y, distance_y, distance_x, pas, New_temps) # appel de la fonction recursive
            else:                               # | une fois la voiture a la haure de l'arrivee
                return Vnx, distance_x, temps   # | on renvoie les donnees dont nous avons besoin

        # affectation des valeurs de la vitesse, de la distance et du temps
        self.__class__.vitesse, self.distance_s, self.__class__.temps = saut_eul(self.__class__.vitesse, 0, distance_y, distance_x, 0.05, self.__class__.temps)

        trajectoire_x = [] # | listes qui vont stocker les valeurs de la distance 
        trajectoire_y = [] # |

        def trajectoire(Vnx, Vny, distance_x, distance_y, pas, temps): # fonction qui va enregistrer toutes les valeurs de la distance
            trajectoire_x.append(distance_x) # | ajout de la valeur de la distance dans la liste
            trajectoire_y.append(distance_y) # |
            # la suite de la fonction est presque identique a la precedente
            if distance_y > -1:
                Vn_1x = pas * ((-self.rho * self.l * self.h * self.Cx * Vnx**2) / (2 * self.m)) + Vnx
                Vn_1y = pas * (((-self.rho * self.l * self.h * self.Cz * Vny**2) / (2 * self.m) - self.g)) + Vny
                New_temps = temps + pas
                distance_y = distance_y + (Vn_1y) * pas
                distance_x = distance_x + (Vn_1x) * pas
                trajectoire(Vn_1x, Vn_1y, distance_x, distance_y, pas, New_temps)

        trajectoire(self.__class__.vitesse, 0, 0, 0, 0.005, self.__class__.temps) # appel de la fonction pour remplir les listes

        plt.plot(trajectoire_x, trajectoire_y) # trace du graphique lineaire
        plt.xlabel('Distance X') # titre des l'axe des abscisses
        plt.ylabel('Distance Y') # titre des l'axe des ordonnees
        plt.title(f'Courbe du saut de la {self.voiture}') # titre du graphique
        plt.show() # affichage de la courbe finale
        
        if self.distance_s < 9 : # verification si la voiture est capadle de passer le ravin
            # affichage de la distance manquante pour passer le ravin
            print(f"La {self.voiture} ne peut pas passer le ravin dans ces conditions.\nElle devrait parcourir {round(9 - self.distance_s,2)} metres de plus pour le franchir.")
            sys.exit() # sortie du programme
        # affichage de la distance a laquelle la voiture a atterit, sa vitesse et le temps qu'elle a mit
        print(f"La {self.voiture} a atterit {round(self.distance_s,2)} metres apres avoir decole, a une vitesse de {round(self.__class__.vitesse,2)} m/s")
        
        
        
    def vitesse_arrivee(self): # creation de la fonction qui va calculer la vitesse a la ligne d'arrivee (vitesse finale)
        def arrivee_eul(Vn,distance,pas,temps): # creation de la fonction recursive
            if distance < 19: # condition initiale
                # equation de la vitesse
                Vn_1 = pas *((-self.rho * self.l * self.h * self.Cx * Vn**2 )/ (2*self.m)- self.mu * self.g + self.aM ) + Vn
                distance_New = Vn_1 * pas + distance # mise a jour de la distance
                temps_a = temps + pas # mise a jour du temps
                return arrivee_eul(Vn_1,distance_New,pas,temps_a) # appel de la fonction recursive
            else:                   # | si la voiture a atteint la ligne d'arrivee
                return Vn, temps    # | on renvoie les valeurs dont nous avons besoin
            
        # affectation des valeurs finales de la vitesse et du temps
        self.__class__.vitesse, self.__class__.temps = arrivee_eul(self.__class__.vitesse,self.distance_s,self.pas,self.__class__.temps)
        # affichage des valeures finales de la vitesse et du temps
        print(f"La {self.voiture} a terminee le circuit en {round(self.__class__.temps, 2)} secondes, et a passee la ligne d'arrivee a une vitesse de {round(self.__class__.vitesse,2)} m/s.")


    
    def afficher_image(self, image_path): # creation de la fonction qui va afficher les images
        img = mpimg.imread(image_path) # utilisation de matplotlib
        plt.imshow(img) # affichage de l'image
        plt.axis('off') # retirer les axes
        plt.show() # afficher l'image finale



    def pente(self): # creation de la fonction qui va realiser les actions a effectuer pour la pente
        self.afficher_image(f'images/Avec frottements/pente/{self.voiture}.png') # rappel du schema et des equations
        time.sleep(5) # marquer un temps d'arret de 5 secondes pour avoir le temps de voir le schema
        self.vitesse_pente() # calcul de la vitesse
       
        
       
    def looping(self): # creation de la fonction qui va realiser les actions a effectuer pour le looping
        self.afficher_image(f'images/Avec frottements/looping/{self.voiture}_debut.png')    # | affichage de la voiture
        time.sleep(5)                                                                       # | dans les differentes parties
        self.afficher_image(f'images/Avec frottements/looping/{self.voiture}_haut.png')     # | du looping avec un temps de pause
        time.sleep(5)                                                                       # | entre chacune d'elles
        self.afficher_image(f'images/Avec frottements/looping/{self.voiture}_fin.png')      # | afin de pouvoir consulter les schemas
        self.vitesse_looping() # calcul de la vitesse
        
        
        
    def saut(self): #creation de la fonction qui va realiser les actions a effectuer pour le saut
        self.afficher_image(f'images/Avec frottements/saut/{self.voiture}.png') # rappel du schema et des equations
        self.vitesse_saut() # calcul de la vitesse



    def arrivee(self): #creation de la fonction qui va realiser les actions a effectuer pour l'arrivee
        self.afficher_image(f'images/Avec frottements/arrivee/{self.voiture}.png') # rappel du schema et des equations
        self.vitesse_arrivee() # calcul de la vitesse


def simulation(): # creation de la fonction principale (elle va appeller les differentes classes en fonction du besoin)
    
    # creation des differents dictionaires afin de repertorier toutes les donnees sur les voitures
    dodge = {"masse" : 1760, "acceleration" : 5.1, "longueur" : 5.28,"largeur" : 1.95,"hauteur" : 1.35,"Cx" : 0.38,"Cz" : 0.3,"mu" : 0.1,"Ucp" : 0.40787394,"Ucl" : 0.411957607}
    toyota = {"masse" : 1615, "acceleration" : 5, "longueur" : 4.51,"largeur" : 1.81,"hauteur" : 1.27,"Cx" : 0.29,"Cz" : 0.3,"mu" : 0.1,"Ucp" : 0.407710617,"Ucl" : 0.41218186}
    chevrolet = {"masse" : 1498, "acceleration" : 5.3, "longueur" : 4.72,"largeur" : 1.88,"hauteur" : 1.3,"Cx" : 0.35,"Cz" : 0.3,"mu" : 0.1,"Ucp" : 0.410226429,"Ucl" : 0.410553047}
    mazda = {"masse" : 1385, "acceleration" : 5.2, "longueur" : 4.3,"largeur" : 1.75,"hauteur" : 1.23,"Cx" : 0.28,"Cz" : 0.3,"mu" : 0.1,"Ucp" : 0.410426269,"Ucl" : 0.408897083}
    nissan = {"masse" : 1540, "acceleration" : 5.8, "longueur" : 4.6,"largeur" : 1.79,"hauteur" : 1.36,"Cx" : 0.34,"Cz" : 0.3,"mu" : 0.1,"Ucp" : 0.408950983,"Ucl" : 0.411192899}
    mitsubishi = {"masse" : 1600, "acceleration" : 5, "longueur" : 4.51,"largeur" : 1.81,"hauteur" : 1.48,"Cx" : 0.28,"Cz" : 0.3,"mu" : 0.1,"Ucp" : 0.408999686,"Ucl" : 0.41015767}
    
    # creation d'un dictionnaire qui va renvoyer vers le dictionnaire conscerne en fonction de la voiture choisie
    voitures = {'dodge': dodge, 'toyota': toyota, 'chevrolet': chevrolet, 'mazda': mazda, 'nissan': nissan, 'mitsubishi': mitsubishi}
    
    Parametres(voitures) # appel de la classe parametres
    
    voiture = Parametres.voiture            # | affectation des donnees choisies a des variables afin de les utiliser depuis l'autre classe
    frottements = Parametres.frottements    # | 
    options = Parametres.options            # | 
    if voiture not in voitures: # verification si la voiture choisie et bien parmis les voitures autorisees 
        print("Voiture invalide")   # | dire a l'utilisateur que la voiture ne correspond pas
        return                      # | et quitter la fonction
    else : # si la voiture existe
        donnees = voitures[voiture] # on accede au bon dictionnaire
        voiture_sim = Simulation(donnees, voiture, frottements, options) # et enfin on appelle la classe Simulation


    voiture_sim.pente()     # | ici, nous allons accedder aux differentes parties de la classe avec un temps d'arret entre chacune
                            # |
    voiture_sim.looping()   # |
                            # |
    voiture_sim.saut()      # |
                            # |
    voiture_sim.arrivee()   # |


simulation() # enfin, nous pouvons lancer la fonction principale afin de demarer la simulation



