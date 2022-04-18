

# MODULES 

# Permet de générer des processus d'interaction avec le system
import subprocess


# FONCTIONS

# Fonction qui met à jour les listes de apt
def majaptget():
    subprocess.call(["apt-get", "update"])

# Fonction qui installe Ansible
def ansibleinstall():
    # Installe le paquet
    subprocess.call(["apt-get", "install", "-y", paquet])
    # si tout se passe bien, l'affiche.
    print("Le service ", paquet, " est installé")



# fonction qui permet la désinstallation d'ansible

def desinstallansible():
    paquet = "ansible"
    # demande si on veut supprimer le paquet
    del_sq = input("Are you sure? (y/n): ")
    # si la réponse est YES
    if del_sq == "y" or del_sq == "Y":
        # passe en sudo, fait un apt-get et purge les dossier ansible et désinstalle
        subprocess.call(["apt-get", "purge", "--auto-remove", paquet])
        # si pas de probléme affiche succés et pass
        print("Succés")
    else:
        pass


########################## MENU ################################################################

# Menu qui permet les installations

while True:
    menu_select = input("""
    1 - Ansible sur ce poste
    2 - Désinstallation ansible sur ce poste
    3 - Sortie\n""")

    if menu_select == "1":
        paquet = "ansible"
        majaptget()
        ansibleinstall()
    elif menu_select == "2":
        majaptget()
        desinstallansible()
    elif menu_select == "3":
        break
    else:
        pass
