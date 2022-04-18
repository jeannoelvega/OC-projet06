# Projet 6 - OpenClassrooms

------

## Script installant divers services sur divers postes en réseau

------

### Pour faire fonctionner ce script, il faut plusieurs prérequis:
* Les serveurs sont tous sous débian ou une distribution basé sur débian.
* Un des serveurs sera le noeud principal où sera installé obligatoirement Ansible.
* Sur le noeud principal, il faut obligatoirement Python version 3.10 ou ultérieur.
* Les autres serveurs auront un acces SSH en root avec le même mot de passe pour tous.
* Les adresses IP des noeuds secondaires seront dans le fichier fichier.txt.
* Les templates d'Ansible seront dans le répertoire playbooks dans le noeud principal.

# Le script ansible.py 

Il permet d'installer automatiquement Ansible sur le noeud principal.

# Le script projet06.py

Ce script permet de selectionner le premier poste libre et d'installer le service choisi.

# Le fichier config.ini

Ce fichier permet de modifier à sa convenance la liste des services.
Le menu affichera cette liste.

le fichier se présente ainsi:
1 http /chemin/fichier/yaml
2 dns /chemin/fichier/yaml

# Le fichier fichier.txt

Ce fichier liste les adresses IP des noeuds secondaires où seront installé les services.

Les adresses IP libres sont indiquées ainsi:
xxx.xxx.xxx.xxx  libre

Les adresses IP utilisées sont indiquées comme suit:
xxx.xxx.xxx.xxx

