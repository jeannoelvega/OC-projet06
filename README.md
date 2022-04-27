# Projet 6 - OpenClassrooms

------

## Script installant divers services sur divers postes en réseau

------

### Pour faire fonctionner ce script, il faut plusieurs prérequis:
* Les serveurs sont tous sous débian ou une distribution basé sur débian.
* Un des serveurs sera le noeud principal où sera installé obligatoirement Ansible.
* Sur le noeud principal, il faut obligatoirement Python version 3.9 ou ultérieur.
* Les autres serveurs auront un acces SSH en root avec le même mot de passe pour tous.
* Les adresses IP des noeuds secondaires seront dans le fichier ipFile.txt.
* Les templates d'Ansible seront dans le répertoire root/playbooks dans le noeud principal.
* l'ensemble des fichiers seront installés et lancés dans le répertoire /root

# Le script projet06.py

Ce script permet de selectionner le premier poste libre et d'installer le service choisi.

# Le fichier config.ini

Ce fichier permet de modifier à sa convenance la liste des services.
Le menu affichera cette liste.

le fichier se présente ainsi:
1 http /chemin/fichier/yaml
2 dns /chemin/fichier/yaml

# Le fichier ipFile.txt

Ce fichier liste les adresses IP des noeuds secondaires où seront installé les services.

Les adresses IP libres sont indiquées ainsi:
xxx.xxx.xxx.xxx  free

Les adresses IP utilisées sont indiquées comme suit:
xxx.xxx.xxx.xxx

