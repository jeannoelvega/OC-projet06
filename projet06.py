# variables globales

global adrIp, adressIp, plbook

# MODULES 

# Permet de lancer des commandes avec le system

import subprocess

# Permet d'utiliser des commandes courantes de tous les OS
import os

# Permet la journalisation et la rotation
import logging
import logging.handlers


# Paramètrage de la journalisation
logging.basicConfig(filename='projet06.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
# code de gestion du logger



# FONCTIONS

# Fonction de nettoyage des fichiers temporaires
def removeTemp():
    if os.path.exists('fichtemp.txt'):
        os.remove('fichtemp.txt')

    if os.path.exists('fichyaml.yml'):
        os.remove('fichyaml.yml')
    logging.info('Nettoyage des fichiers temporaires effectuée')


# Fonction qui récupère l'adresse IP d'une machine libre
def choixserver():
    chaine = "libre"  # text à rechercher
    try:
        fichtemp = open("fichtemp.txt", "r")  # ouvre le fichier txt temporaire
        ipfind = False      # pour l'instant, on n'a pas trouvé d'IP
        for ligne in fichtemp:  #  parcoure fichtemp.txt
            if chaine in ligne: #  si on trouve le mot "libre"...
                ipfind = True   #  ...c'est qu'on a une adresse IP
                global adressIp
                adressIp = ligne.split()    # découpe la ligne en liste de str
                adressIp.remove( "libre")   # enleve le mot "libre" de la liste 
                global adrIp
                adrIp = adressIp
                break
        fichtemp.close()
    except:
        logging.error('une erreur est survenu ligne 36 à 47')

    if ipfind == False:     #  si on n'a pas trouvé d'adresse IP libre
        print("il n'y a plus de machines libres")
        logging.info("il n'y a plus de machine libre")
        exit()

    logging.info('IP libre trouvé')
    return adrIp

# Fonction qui modifie la ligne ou l'IP était libre en IP non libre
def modifIp():
    global adrIp                 
    adrIp = ' '.join(adrIp)                 # met en format str
    chaine = adrIp  
    try:
        fichtemp = open("fichtemp.txt", "r")    # ouvre le fichier temporaire en lecture seule
        fichier = open("fichier.txt", "w")      # ouvre fichier.txt en écriture
        for ligne in fichtemp:                  # lis chaque ligne de fichtemp dans une boucle for
            if chaine in ligne:                 # si l'adresse IP est dans la ligne...
                adressIp = ligne.split()        # découpe la ligne en liste de str
                adressIp.remove( "libre")       # enleve le mot "libre" de la liste
                adressIp = ' '.join(adressIp)   # transforme la liste en str
                adressIp = adressIp + "\n"      # ajoute un saut de ligne
                ligne = adressIp                # met la valeur dans la variable ligne
            fichier.write(ligne)                # écrit la ligne dans le fichier texte
        fichtemp.close()                        # ferme le fichier temporaire
        fichier.close()                         # ferme fichier.txt
    except:
        logging.error('Problème avec les fichiers fichtemp.txt et/ou fichier.txt')

    logging.info('fichier.txt modifié')

# Fonction qui crée le fichier yaml temporaire pour lancer la commande Ansible
def createFichyaml():
    global adrIp
    try:
        fichier = open(plbook, "r")             # ouvre le template yaml en lecture
        lignes = fichier.readlines()            # enregistre chaque ligne dans une liste
        fichier.close()                         # ferme le template yaml
        lignes[1] = "- hosts: " + adrIp + "\n"  # modifie la seconde ligne avec l'adresse IP trouvé
    except:
        logging.error('chemin non valide')


    
    try:
        fichtemp = open("fichyaml.yml", "w")    # ouvre le fichier yaml temporaire
        fichtemp.writelines(lignes)             # recopie les lignes
        fichtemp.close()                        # ferme le fichier yaml temporaire
    except:
        logging.error("Problème d'écriture dans le fichier fichyaml.yml")

    logging.info('Création du fichier yaml terminée')

# Fonction qui crée un fichier temporaire pour la recherche d'une machine libre 
# et pour modifier cette machine en occupé.
def copyfich():
# copie le fichier des adresses IP à l'identique dans un fichier temporaire
    try:
        fichier = open("fichier.txt", "r")
        fichtemp = open("fichtemp.txt", "w")
        fichtemp.write(fichier.read() )
        fichier.close()
        fichtemp.close()
    except:
        logging.error('problème de copie de fichier.txt vers fichtemp.txt')

    logging.info('Création du fichier temporaire txt terminée')

# Fonction qui installe les playbooks
def installplaybook():
    try:
        subprocess.call(["ansible-playbook", "/root/fichyaml.yml"])
        print("Service instalé à l'adresse ", adrIp)
        logging.info("Service instalé à l'adresse ", adrIp)
    except:
        logging.error('Problème avec le lancement du playbook fichyaml.yml')

# Fonction principal qui lance les autres fonctions dans l'ordre
def principal():

    copyfich()
    choixserver()
    modifIp()
    createFichyaml()
    #installplaybook()
    #removeTemp()

########################## MENU ################################################################

logging.info('démarrage de projet06.py')
# Création des dictionnaires vides
listService = {}
listPlaybook = {}

# Remplissage des dictionnaires avec notre menu
try:
    fileini = open("config.ini", "r")       #fichier de configuration de notre menu
    for line in fileini :
        key = int(line.split()[0])
        name = line.split()[1]
        path = line.split()[2]
        listService[key] = name
        listPlaybook[key] = path
    fileini.close()
except:
    logging.error('problème avec le fichier config.ini')

# récupère le nombre d'items dans notre menu
tailleDic = len(listService)

# affiche notre menu
for key, val in listService.items():
    print(key, " - ", val)

print(0, " - sortie")   # Rajoute la sortie du programme

# Boucle de choix avec gestion des erreurs
inputVal = input("Faites votre choix ")
inputVal = int(inputVal)
if inputVal == 0:
    exit(0)
elif inputVal > tailleDic:
    print("Ce choix n'est pas dans la liste")
else:
#    print(listPlaybook[inputVal])
    plbook = listPlaybook[inputVal]
#    plbook = "squid.yml"       # Pour tests
    principal()

