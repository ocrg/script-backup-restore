# Projet 6
![license](https://img.shields.io/badge/license-CC0-green) _ce code totalement libre._

Ce script permet de faire un backup d'un site WordPress, de ses fichiers essentiels et de sa base de donnée MySQL. Autrement dit, il permet de repartir à zéro. Il permet également de faire une restauration à partir de l'un des backups effectué.


## Pour commencer

Le script fonctionne dans le contexte ci-dessous.

### Contexte

Sur une VM [Debian 11](https://www.debian.org) créée avec VirtualBox 6.1, le site est installé avec les programmes suivants :

- Apache2
- PHP 7
- mysql 8
- WordPress [téléchargé](https://fr.wordpress.org/download/) sur le site
- Python 3

Une fois le site installé et fonctionnel, il faut le personnaliser en choisissant un thème, et en publiant quelques billets pour rendre le site un peu plus "vivant".

### Quelques détails

Pour installer le site, on peut utiliser des tutoriels. En voici quelques-uns :
- [netpunet.fr](https://fr.wordpress.org/download/), surtout MySQL,
- [reportingbusiness](https://www.reportingbusiness.fr/blogging/installez-wordpress-sur-votre-ordinateur-en-moins-de-15-minutes-linux.html), surtout Apache2,
- [wordpress.org](https://fr.wordpress.org/support/article/how-to-install-wordpress/), surtout pour WordPress mais pas que.

Du reste il y a sur [OpenClassrooms](https://openclassrooms.com/fr/) les cours sur LAMP, MySQL, WordPress, Linux et la virtualisation.

## Présentation du script

Le fichier svg.py est le script qui effectue l'opération voulue, avec les variables contenus dans fichier config.yaml.

Le fichier config.yaml est le fichier de configuration. Il contient notamment les variables, et l'opération à effectuer (voir plus bas) : un backup ou une restauration.

En somme, si le script est le moteur, son fichier de configuration est le conducteur.

### config.yaml

Le fichier de configuration, est divisé en 3 petites parties.

La première partie du fichier, le bloque de commentaires, sont des indications propres au format YAML.

La seconde partie sont des précisions sur le langage du script, et surtout la version de python utilisée ainsi que l'OS et sa version.

La troisième concerne les constantes utilisées dans le script.
La dernière est particulière, il faut écrire ``backup`` si on veut qu'une backup soit effectuée, ou ``restore`` si on veut que ce soit une restauration. Par défaut, c'est une backup qui est effectuée.

### svg.py

Le meilleur moyen pour comprendre le fonctionnement du script est d'aller le regarder et d'y lire les commentaires. Le script est divisé en plusieurs grandes parties qui sont elles mêmes divisées en sous-parties.

Voici l'arborescence :
- les imports
- fonction de lecture du fichier .yaml
- partie backup
  - fonction de création d'un dossier temporaire
  - fonction de sauvegarde de la base de données dans le dossier temporaire
  - fonction de copie des fichiers à sauvegarder dans le dossier temporaire
  - fonction de compression du dossier temporaire, et qui supprime ensuite ce dossier
- partie restauration
  - fonction de création d'un dossier temporaire
  - fonction qui supprime les fichiers à restaurer (simulation d'un crash)
  - fonction de décompression, tout est placé dans le dossier temporaire
  - fonction de restauration des fichiers et dossiers, les éléments sont copier du dossier temporaire au répertoire du site
  - fonction de restauration de la base de donnée MySQL, et qui supprime le dossier temporaire
- fonction backup (cette fonction lance les fonctions écrites dans la partie backup)
- fonction restauration (cette fonction lance les fonctions écrites dans la partie restauration)
- morceau de code qui remplie les constantes (il utilise vars et la fonction de lecture du fichier .yaml pour remplir lesdites constantes)

## Utilisation

Une fois la configuration ajustée, on peut lancer le script. Ce dernier quant à lui n'a logiquement pas besoin d'être modifié.

Il faut ouvrir le terminal et écrire cette ligne de commande :

``python3 svg.py config.yaml``

## Outils utilisés :

**gedit 3.38.1** avec des greffons déjà présents.

**Debian 11** avec Gnome en environnement de bureau.

## Version

Version actuelle stable : 1.0 
Écrite à la fin de l'été 2021. 
Dernière mise à jour : voir les commits. 

Des mises à jour très mineures peuvent avoir lieu mais rien de significatif.
